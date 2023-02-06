import json
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from users.validation import validate_email, validate_password
from users.models import User
from users.serializers import SignUpSerializer



# 회원가입

class SignUp(APIView):
    def post(self, request):
        data=request.data
        serializer = SignUpSerializer(data=data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True는 유효성 검사시 에러 메세지를 가시적으로 클라이언트 측에 전달하는 역할
            serializer.save()
            return Response({"message":"회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 마이페이지
       
class MypageView(APIView):

    def get(self, request, user_id):  # 개인 프로필 정보 불러오기
        user = get_object_or_404(User, id=user_id)
        serializer = MypageSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id): # 회원탈퇴
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response('사용자 삭제 완료',status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('권한이 없습니다', status=status.HTTP_403_FORBIDDEN)








        data = json.loads(request.body)
        try :
            name = data['name']
            email = data['email']
            password = data['password']
            phone_number = data['phone_number']

            if validate_email(email) == False :
                return JsonResponse({'MESSAGE':'INVALID_EMAIL_ADDRESS'}, status=400)
            
            if validate_password(password) == False :
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)
            
            if User.objects.filter(email = email).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS_EMAIL'}, status=400)
            
            User.objects.create(
                name = name,
                email = email,
                password = password,
                phone_number = phone_number,
            )

            return JsonResponse({'MESSAGE':'SUCCESS'} , status = 201)

        except KeyError :
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status = 400)
