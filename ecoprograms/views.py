from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404 
from .models import Ecoprogram, Review, EcoprogramApply
from .serializers import (EcoprogramReviewSerializer, EcoprogramReviewCreateSerializer, EcoprogramSerializer,
                        EcoprogramListSerializer, EcoprogramEnrollSerializer, EcoprogramEditSerializer, EcoprogramReviewEditSerializer)


# 에코프로그램 리뷰 

class EcoprogramReviewView(APIView): # 리뷰 전체 (조회)

    def get(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        review = ecoprogram.review_ecoprogram.all()
        serializer = EcoprogramReviewSerializer(review, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EcoprogramReviewCreateView(APIView): # 리뷰 (등록)

    def post(self, request, ecoprogram_id):
        serializer = EcoprogramReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, ecoprogram_id=ecoprogram_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EcoprogramReviewDetailView(APIView): # 작성한 리뷰 (수정, 삭제)
    
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

class EcoproramView(APIView): # 전체 에코프로그램 (조회)

    def get(self, request):
        ecoprogram = Ecoprogram.objects.all()
        print(ecoprogram)
        serializer = EcoprogramListSerializer(ecoprogram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EcoprogramEnrollView(APIView): # 에코프로그램 (등록)

    def post(self, request):
        serializer = EcoprogramEnrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(host=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EcoprogramDetailView(APIView): # 해당 에코프로그램 상세 페이지 (조회, 수정, 삭제)

    def get(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        serializer = EcoprogramSerializer(ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, ecoprogram_id):
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user == ecoprogram.host:
            serializer = EcoprogramEditSerializer(ecoprogram, data=request.data)
            if serializer.is_valid():
                serializer.save()
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
