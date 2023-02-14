from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 


urlpatterns = [
    # 로그인, 회원가입
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh token
    path('signup/', views.SignUpView.as_view(), name='signup_view'),
    # path('kakao/callback/'),
    # path('google/callback/'),
    
    # 마이페이지(소비자)
    path('consumer/<int:user_id>/', views.MypageConsumerInfoView.as_view(), 
        name='mypage_consumer_info_view'), # 프로필 정보 불러오기
    
    path('consumer/<int:user_id>/', views.MypageConsumerProfileEditView.as_view(), 
        name='mypage_consumer_profile_edit_view'), # 프로필 정보 수정
    
    path('consumer/<int:user_id>/applied/', views.MypageEcoprogramAppliedView.as_view(), 
        name='mypage_ecoprogram_applied_view'), # 신청한 에코프로그램
    
    path('consumer/<int:user_id>/confirmed/', views.MypageEcoprogramConfirmedView.as_view(), 
        name='mypage_ecoprogram_confirmed_view'), # 참여확정된 에코프로그램
    
    path('consumer/<int:user_id>/likes/', views.MypageEcoprogramLikeView.as_view(), 
        name='mypage_ecoprogram_like_view'), # 좋아요한 에코프로그램
    
    # 마이페이지(환경단체)
    path('organization/<int:user_id>/', views.MypageOrganizationInfoView.as_view(), 
        name='mypage_organization_info_view'), # 프로필 정보 불러오기

    path('organization/<int:user_id>/', views.MypageOrganizationProfileEditView.as_view(), 
        name='mypage_organization_profile_edit_view'), # 프로필 정보 수정

    path('organization/<int:user_id>/created/', views.MypageEcoprogramCreatedView.as_view(), 
        name='mypage_ecoprogram_created_view'), # 생성한 에코프로그램 불러오기

    path('organization/<int:user_id>/created/<int:ecoprogram_id>/', views.MypageEcoprogramApproveRejectionView.as_view(), 
        name='mypage_ecoprogram_approve_rejection_view'), # 해당 에코프로그램 신청 인원 관리(승인/거절)

    path('organization/<int:user_id>/upcyclings/', views.MypageUpcyclingCompanyManagementView.as_view(), 
        name='mypage_upcycling_company_management_view'), # 업사이클링 업체 등록 관리
]