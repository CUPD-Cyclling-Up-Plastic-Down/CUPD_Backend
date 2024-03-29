from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import get_object_or_404 
from .models import Ecoprogram, Review, EcoprogramApply
from .serializers import (EcoprogramReviewSerializer, EcoprogramReviewCreateSerializer, EcoprogramSerializer,
                        EcoprogramListSerializer, EcoprogramEnrollSerializer, EcoprogramEditSerializer, EcoprogramReviewEditSerializer)
from .pagination import PaginationHandlerMixin



# 에코프로그램 리뷰 

class EcoprogramReviewPagination(PageNumberPagination): # 에코프로그램 리뷰 페이지네이션
    page_size = 10
    page_query_param = 'page'


class EcoprogramReviewView(APIView, PaginationHandlerMixin): # 에코프로그램 리뷰 전체 (조회)
    permission_classes = [AllowAny]
    pagination_class = EcoprogramReviewPagination
    serializer_class = EcoprogramReviewSerializer

    def get(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        review = ecoprogram.review_ecoprogram.all()
        page = self.paginate_queryset(review)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = EcoprogramReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EcoprogramReviewCreateView(APIView): # 에코프로그램 리뷰 (등록)

    def post(self, request, ecoprogram_id):
        serializer = EcoprogramReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, ecoprogram_id=ecoprogram_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EcoprogramReviewDetailView(APIView): # 에코프로그램 리뷰 (수정, 삭제)
    
    def put(self, request, ecoprogram_id, review_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            serializer = EcoprogramReviewEditSerializer(review, data=request.data) 
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ecoprogram_id, review_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
            return Response({"msg":"해당 리뷰가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


# 에코프로그램

class EcoprogramPagination(PageNumberPagination): # 에코프로그램 페이지네이션
    page_size = 6
    page_query_param = 'page'


class EcoproramView(ModelViewSet, PaginationHandlerMixin): # 에코프로그램 전체 (조회)
    permission_classes = [AllowAny]
    pagination_class = EcoprogramPagination
    serializer_class = EcoprogramListSerializer
    queryset = Ecoprogram.objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter]
    search_fields = ['id','title','content','organization',]

    def get(self, request):
        sort = request.GET.get('sort','')
        if sort == 'likes':
            self.queryset = Ecoprogram.objects.all().annotate(likes_count=Count('likes')).order_by('-likes_count')
        elif sort == 'views':
            self.queryset = Ecoprogram.objects.all().order_by('-views')
    
        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = EcoprogramListSerializer(page, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   # return self.get_paginated_response(serializer.data)  # (참고) if-else문을 써도 되고 if-else 지우고 주석처리한 코드를 사용해도 무방


class EcoprogramEnrollView(APIView): # 에코프로그램 (등록)

    def post(self, request):
        serializer = EcoprogramEnrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EcoprogramDetailView(APIView): # 해당 에코프로그램 상세 페이지 (조회, 수정, 삭제)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        serializer = EcoprogramSerializer(ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user == ecoprogram.host:
            serializer = EcoprogramEditSerializer(ecoprogram, data=request.data)
            if serializer.is_valid():
                serializer.save(host=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user == ecoprogram.host: 
            ecoprogram.delete()
            return Response({"msg":"게시물이 삭제되었습니다."},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class EcoprogramDetailLikeView(APIView): # 해당 프로그램 '좋아요'

    def post(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user in ecoprogram.likes.all():
            ecoprogram.likes.remove(request.user)
            return Response({"msg":"에코프로그램 좋아요를 취소했습니다."}, status=status.HTTP_200_OK)
        else: 
            ecoprogram.likes.add(request.user)
            return Response({"msg":"에코프로그램을 좋아요했습니다."}, status=status.HTTP_200_OK)


class EcoprogramDetailApplyView(APIView): # 해당 프로그램 상세 페이지에서 '신청'하기

    def post(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user == ecoprogram.host:
            return Response({"msg":"해당 ecoprogram의 host는 참가신청할 수 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        elif request.user != ecoprogram.host: 
            max_guest = ecoprogram.max_guest
            approve_guest = EcoprogramApply.objects.filter(ecoprogram=ecoprogram_id, result='APPROVE').count()
            if max_guest == approve_guest:
                return Response({"msg":"모집이 마감되었습니다."}, status=status.HTTP_200_OK)
            if request.user in ecoprogram.participant.all():
                ecoprogram.participant.remove(request.user)
                return Response({"msg":"에코프로그램 신청을 취소했습니다."}, status=status.HTTP_200_OK)
            else:
                EcoprogramApply.objects.create(guest=request.user, ecoprogram=ecoprogram, result='WAITING')
                return Response({"msg":"에코프로그램 신청을 접수했습니다."}, status=status.HTTP_200_OK)
            


