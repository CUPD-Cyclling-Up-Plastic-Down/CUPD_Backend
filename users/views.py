import json
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User
from users.serializers import SignUpSerializer
from .serializers import MypageConInfoSerializer, MypageOrgInfoSerializer, MyTokenObtainPairSerializer



# 회원가입

class SignUpView(APIView):
    def post(self, request):
        data=request.data
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True는 유효성 검사시 에러 메세지를 가시적으로 클라이언트 측에 전달하는 역할
            serializer.save()
            return Response({"message":"회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# jWT token 로그인

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 마이페이지
       
class MypageConInfoView(APIView): # (소비자): 개인 프로필 정보 불러오기, 회원탈퇴

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = MypageConInfoSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response('회원탈퇴 완료',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)


class MypageOrgInfoView(APIView): # (환경단체): 개인 프로필 정보 불러오기, 회원탈퇴

    def get(self, request, user_id): 
        user = get_object_or_404(User, id=user_id)
        serializer = MypageOrgInfoSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response('사용자 삭제 완료',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)
