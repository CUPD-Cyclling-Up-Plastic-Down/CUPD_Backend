from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    SignUpConsumerSerializer, SignUpOrganizationSerializer, MypageConsumerInfoSerializer, 
    MypageOrganizationInfoSerializer, MyTokenObtainPairSerializer, MypageEcoprogramAppliedSerializer, 
    MypageEcoprogramConfirmedSerializer, MypageEcoprogramLikeSerializer, MypageEcoprogramCreatedSerializer, 
    MypageConsumerProfileEditSerializer, MypageOrganizationProfileEditSerializer,MypageEcoprogramApplyResultSerializer
)
from ecoprograms.models import Ecoprogram, EcoprogramApply
from upcyclings.models import UpcyclingCompany
from upcyclings.serializers import UpcyclingCompanyManagementSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly


# 회원가입(소비자)

class SignUpConsumerView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = SignUpConsumerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"(소비자) 회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# 회원가입(환경단체)

class SignUpOrganizationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpOrganizationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"msg":"(환경단체) 회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"msg":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)


# jWT token 로그인

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# 마이페이지(소비자)

class MypageConsumerInfoView(APIView): # (소비자): 프로필 정보 (조회, 회원탈퇴)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = MypageConsumerInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class MypageEcoprogramAppliedView(APIView): # (소비자): 신청한 에코프로그램 전체 (조회)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        applied_ecoprogram = user.ecoprogram_apply_guest.all()
        serializer = MypageEcoprogramAppliedSerializer(applied_ecoprogram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

class MypageEcoprogramAppliedDetailView(APIView): # (소비자): 신청한 에코프로그램 개별 (조회, 삭제)

    def get(self, request, user_id, ecoprogram_apply_id):
        user = get_object_or_404(User, id=user_id)
        applied_ecoprogram = user.ecoprogram_apply_guest.get(id=ecoprogram_apply_id)
        serializer = MypageEcoprogramAppliedSerializer(applied_ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id, ecoprogram_apply_id):
        user = get_object_or_404(User, id=user_id)
        applied_ecoprogram = user.ecoprogram_apply_guest.get(id=ecoprogram_apply_id)
        if request.user == user:
            applied_ecoprogram.delete()
            return Response({"msg":"삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramConfirmedView(APIView): # (소비자): 참여확정된 에코프로그램 전체 (조회)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        applied_ecoprogram = user.ecoprogram_apply_guest.filter(result='APPROVE')
        serializer = MypageEcoprogramAppliedSerializer(applied_ecoprogram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageEcoprogramConfirmedDetailView(APIView): # (소비자): 참여확정된 에코프로그램 개별 (조회, 삭제)

    def get(self, request, user_id, ecoprogram_apply_id):
        user = get_object_or_404(User, id=user_id)
        confirmed_ecoprograms = user.ecoprogram_apply_guest.filter(result='APPROVE')
        confirmed_ecoprogram = confirmed_ecoprograms.get(id=ecoprogram_apply_id)
        serializer = MypageEcoprogramConfirmedSerializer(confirmed_ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)
            

    def delete(self, request, user_id, ecoprogram_apply_id):
        user = get_object_or_404(User, id=user_id)
        confirmed_ecoprograms = user.ecoprogram_apply_guest.filter(result='APPROVE')
        confirmed_ecoprogram = confirmed_ecoprograms.get(id=ecoprogram_apply_id)
        if request.user == user:
            confirmed_ecoprogram.delete()
            return Response({"msg":"삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramLikeView(APIView): # (소비자): 좋아요 한 에코프로그램

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        likes_ecoprogram = user.ecoprogram_likes.all()
        if request.user == user:
            serializer = MypageEcoprogramLikeSerializer(likes_ecoprogram, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"좋아요 한 에코프로그램이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

    

# 마이페이지(환경단체)

class MypageOrganizationInfoView(APIView): # (환경단체): 프로필 정보 (조회, 삭제)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = MypageOrganizationInfoSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if request.user == user:
            user.delete()
            return Response({"msg":"회원탈퇴 완료"},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다"}, status=status.HTTP_403_FORBIDDEN)


class MypageOrganizationProfileEditView(APIView): # (환경단체): 프로필 정보(수정)

    def patch(self, request, user_id):
        serializer = MypageOrganizationProfileEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MypageEcoprogramCreatedView(APIView): # (환경단체): 생성한 에코프로그램 전체 (조회)
    
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        created_ecoprogram = user.ecoprogram_host.all()
        serializer = MypageEcoprogramCreatedSerializer(created_ecoprogram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageEcoprogramCreatedDetailView(APIView): # (환경단체): 생성한 에코프로그램 개별 (조회, 삭제)
    
    def get(self, request, user_id, ecoprogram_id):
        user = get_object_or_404(User, id=user_id)
        created_ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        serializer = MypageEcoprogramCreatedSerializer(created_ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id, ecoprogram_id):
        user = get_object_or_404(User, id=user_id)
        created_ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        if request.user == user:
            created_ecoprogram.delete()
            return Response({"msg":"삭제 되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramApplyResultView(APIView): # (환경단체): 해당 에코프로그램 신청 결과 (전체 조회, 권한 설정)

    def get(self, request, ecoprogram_id, user_id):
        user = get_object_or_404(User, id=user_id)
        ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        applied_ecoprogram = ecoprogram.ecoprogram_apply.all()
        serializer = MypageEcoprogramApplyResultSerializer(applied_ecoprogram, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, ecoprogram_id, user_id): # 권한 설정
        user = get_object_or_404(User, id=user_id)
        ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        if request.user == ecoprogram.host: 
            guest = request.data['guest']
            result = request.data['result']
            ecoprogram_apply = EcoprogramApply.objects.get(guest=guest, ecoprogram=ecoprogram)
            ecoprogram_apply.result = f'{result}'
            ecoprogram_apply.save()
            return Response({"msg":f"에코프로그램 신청을 {result}했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


class MypageEcoprogramApplyResultDetailView(APIView): # (환경단체): 해당 에코프로그램 신청 결과 (개별 조회, 인원 삭제)

    def get(self, request, ecoprogram_id, user_id, guest_id):
        user = get_object_or_404(User, id=user_id)
        ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        applied_ecoprogram = ecoprogram.ecoprogram_apply.get(guest_id=guest_id)
        serializer = MypageEcoprogramApplyResultSerializer(applied_ecoprogram)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, ecoprogram_id, user_id, guest_id):
        user = get_object_or_404(User, id=user_id)
        ecoprogram = user.ecoprogram_host.get(id=ecoprogram_id)
        if request.user == ecoprogram.host:
            ecoprogram_guest = ecoprogram.ecoprogram_apply.get(guest_id=guest_id)
            ecoprogram_guest.delete()
            return Response({"msg":"해당 인원 신청내역이 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
            

class MypageUpcyclingCompanyManagementView(APIView): # (환경단체): 업사이클링 업체 등록 관리 (전체 조회)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        upcyclingcompany = user.upcyclingcompany_registrant.all()
        serializer = UpcyclingCompanyManagementSerializer(upcyclingcompany, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MypageUpcyclingCompanyManagementDetailView(APIView): # (환경단체): 업사이클링 업체 등록 관리 (개별 조회, 삭제)

    def get(self, request, user_id, upcyclingcompany_id):
        user = get_object_or_404(User, id=user_id)
        upcyclingcompany = user.upcyclingcompany_registrant.get(id=upcyclingcompany_id)
        serializer = UpcyclingCompanyManagementSerializer(upcyclingcompany)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id, upcyclingcompany_id):
        user = get_object_or_404(User, id=user_id)
        upcyclingcompany = user.upcyclingcompany_registrant.get(id=upcyclingcompany_id)
        if request.user == upcyclingcompany.registrant:
            upcyclingcompany.delete()
            return Response({"msg":"해당 업사이클링 업체가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"msg":"권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)


