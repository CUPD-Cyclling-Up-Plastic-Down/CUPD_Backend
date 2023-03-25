from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404 
from .models import UpcyclingCompany
from .serializers import UpcyclingCompanyListSerializer, UpcyclingCompanySerializer, UpcyclingCompanyEnrollSerializer


class UpcyclingCompanyListView(APIView): # 전체 업사이클링 업체 조회

    def get(self, request):
        upcyclingcompany = UpcyclingCompany.objects.all()
        serializer = UpcyclingCompanyListSerializer(upcyclingcompany, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpcyclingCompanyDetailView(APIView): # 해당 업사이클링 업체 상세 페이지 (조회, 수정, 삭제)

    def get(self, request, upcyclingcompany_id):
        upcyclingcompany = get_object_or_404(UpcyclingCompany, id=upcyclingcompany_id)
        serializer = UpcyclingCompanySerializer(upcyclingcompany)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, company_id):
        upcyclingcompany = get_object_or_404(UpcyclingCompany, id=company_id)
        if request.user == upcyclingcompany.registrant:
            serializer = UpcyclingCompanySerializer(upcyclingcompany, data=request.data)
            if serializer.is_valid(): 
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK) 
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, company_id):
        upcyclingcompany = get_object_or_404(UpcyclingCompany, id=company_id)
        if request.user == upcyclingcompany.host: 
            upcyclingcompany.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class UpcyclingCompanyEnrollView(APIView): # 업사이클링 업체 (등록)

    def post(self, request):
        serializer = UpcyclingCompanyEnrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(registrant=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

