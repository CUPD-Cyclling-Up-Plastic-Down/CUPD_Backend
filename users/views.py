from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    SignUpSerializer, MypageConsumerInfoSerializer, MypageOrganizationInfoSerializer, MyTokenObtainPairSerializer, 
    MypageEcoprogramAppliedSerializer, MypageEcoprogramConfirmedSerializer, MypageEcoprogramLikeSerializer,
    MypageEcoprogramCreatedSerializer, MypageEcoprogramApproveRejectSerializer, MypageConsumerProfileEditSerializer,
    MypageOrganizationProfileEditSerializer
)
from ecoprograms.models import Ecoprogram, EcoprogramApply
from upcyclings.models import UpcyclingCompany
from upcyclings.serializers import UpcyclingCompanyManagementSerializer


# 회원가입

class SignUpView(APIView):

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True): # raise_exception=True는 유효성 검사시 에러 메세지를 가시적으로 클라이언트 측에 전달하는 역할
            serializer.save()
            return Response({"msg":"회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# jWT token 로그인

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 마이페이지(소비자)

class MypageConsumerInfoView(APIView):

    def get(self, request, user_id): # (소비자): 프로필 정보 (조회)
    
        user = get_object_or_404(User, id=user_id)
        serializer = MypageConsumerInfoSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id): # 회원탈퇴
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response({"msg":"회원탈퇴 완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


class MypageConsumerProfileEditView(APIView): # (소비자): 프로필 정보 (수정)

    def patch(self, request, user_id):
        serializer = MypageConsumerProfileEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MypageEcoprogramAppliedView(APIView): # (소비자): 신청한 에코프로그램(조회, 삭제)

    def get(self, request, user_id): # 조회
        user = get_object_or_404(User, id=user_id)
        serializer = MypageEcoprogramAppliedSerializer(user, many=True)
        return Response(serializer.data)

    def delete(self, request, participant_id): # 삭제
        participant = get_object_or_404(Ecoprogram, id=participant_id)
        if request.user == participant:
            participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramConfirmedView(APIView): # (소비자): 참여확정된 에코프로그램

    def get(self, request, user_id): # 조회
        user = get_object_or_404(User, id=user_id)
        serializer = MypageEcoprogramConfirmedSerializer(user, many=True)
        if request.data['result'] == '승인':
            return Response(serializer.data)

    def delete(self, request, participant_id): # 삭제
        participant = get_object_or_404(Ecoprogram, id=participant_id)
        if request.user == participant:
            participant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramLikeView(APIView): # (소비자): 좋아요한 에코프로그램

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = MypageEcoprogramLikeSerializer(user, many=True)
        # if request.data['likes']:
        return Response(serializer.data)

    



# 마이페이지(환경단체)

class MypageOrganizationInfoView(APIView): 

    def get(self, request, user_id): # 프로필 정보(조회)
        user = get_object_or_404(User, id=user_id)
        serializer = MypageOrganizationInfoSerializer(user)
        return Response(serializer.data)

    def delete(self, request, user_id): # 회원탈퇴
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response({"msg":"회원탈퇴 완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


class MypageOrganizationProfileEditView(APIView): # 프로필 정보(수정)

    def patch(self, request, user_id):
        serializer = MypageOrganizationProfileEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MypageEcoprogramCreatedView(APIView): # (환경단체): 생성한 에코프로그램
    
    def get(self, request, user_id): # 조회
        user = get_object_or_404(User, id=user_id)
        serializer = MypageEcoprogramCreatedSerializer(user, many=True)
        if request.data['host'] == request.user:
            return Response(serializer.data)

    def delete(self, request, host_id): # 삭제
        host = get_object_or_404(Ecoprogram, id=host_id)
        if request.user == host:
            host.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramApproveRejectView(APIView):

    def get(self, request, user_id): # 해당 에코프로그램 신청 인원 (조회)
        user = get_object_or_404(User, id=user_id)
        serializer = MypageEcoprogramApproveRejectSerializer(user, many=True)
        return Response(serializer.data)

    def put(self, request, ecoprogram_id): # 해당 에코프로그램 신청 인원 (처리) (승인/거절 여부 결정)
        ecoprogram = get_object_or_404(Ecoprogram, id=ecoprogram_id)
        if request.user == ecoprogram.host: 
            guest = request.data['guest'] # 특정 신청자
            result = request.data['result'] # 신청결과
            ecoprogram_apply = EcoprogramApply.objects.get(guest=guest, ecoprogram=ecoprogram)
            ecoprogram_apply.result = f'{result}'
            ecoprogram_apply.save()
            return Response({"msg":f"워크샵 신청을 {result}했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, guest_id): # 해당 에코프로그램 신청 인원 (삭제)
        guest = get_object_or_404(EcoprogramApply, id=guest_id)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MypageUpcyclingCompanyManagementView(APIView): # (환경단체): 업사이클링 업체 등록 관리

    def get(self, request, registrant_id): # 조회
        registrant = get_object_or_404(UpcyclingCompany, id=registrant_id)
        serializer = UpcyclingCompanyManagementSerializer(registrant)
        return Response(serializer.data)

    def delete(self, request, registrant_id): # 삭제
        registrant = get_object_or_404(UpcyclingCompany, id=registrant_id)
        if request.user == registrant.registrant:
            registrant.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


