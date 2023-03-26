from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 


urlpatterns = [
    # 로그인, 회원가입
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT access token 발급
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # JWT refresh token 발급
    path('signup/consumer/', views.SignUpConsumerView.as_view(), name='signup_view'), # 회원가입(소비자)
    path('signup/organization/', views.SignUpOrganizationView.as_view(), name='signup_view'), # 회원가입(환경단체)
    # path('kakao/callback/'),
    # path('google/callback/'),
    
    # 마이페이지(소비자)
    path('consumer/<int:user_id>/', views.MypageConsumerInfoView.as_view(), 
        name='mypage_consumer_info_view'), # 프로필 정보 (조회, 삭제)
    
    path('consumer/<int:user_id>/', views.MypageConsumerProfileEditView.as_view(), 
        name='mypage_consumer_profile_edit_view'), # 프로필 정보 (수정)
    
    path('consumer/<int:user_id>/applied/', views.MypageEcoprogramAppliedView.as_view(), 
        name='mypage_ecoprogram_applied_view'), # 신청한 에코프로그램 전체 (조회)

    path('consumer/<int:user_id>/applied/<int:ecoprogram_apply_id>/', views.MypageEcoprogramAppliedDetailView.as_view(), 
        name='mypage_ecoprogram_applied_detail_view'), # 신청한 에코프로그램 개별 (조회, 삭제)
    
    path('consumer/<int:user_id>/confirmed/', views.MypageEcoprogramConfirmedView.as_view(), 
        name='mypage_ecoprogram_confirmed_view'), # 참여확정된 에코프로그램 전체 (조회, 삭제)

    path('consumer/<int:user_id>/confirmed/<int:ecoprogram_apply_id>/', views.MypageEcoprogramConfirmedDetailView.as_view(), 
        name='mypage_ecoprogram_confirmed_detail_view'), # 참여확정된 에코프로그램 개별 (조회, 삭제)
    
    path('consumer/<int:user_id>/likes/', views.MypageEcoprogramLikeView.as_view(), 
        name='mypage_ecoprogram_like_view'), # 좋아요한 에코프로그램 (조회)
    
    # 마이페이지(환경단체)
    path('organization/<int:user_id>/', views.MypageOrganizationInfoView.as_view(), 
        name='mypage_organization_info_view'), # 프로필 정보 (조회, 삭제)

    path('organization/<int:user_id>/', views.MypageOrganizationProfileEditView.as_view(), 
        name='mypage_organization_profile_edit_view'), # 프로필 정보 (수정)

    path('organization/<int:user_id>/ecoprogram/created/', views.MypageEcoprogramCreatedView.as_view(), 
        name='mypage_ecoprogram_created_view'), # 생성한 에코프로그램 (조회, 삭제)

    path('organization/<int:user_id>/ecoprogram/created/<int:ecoprogram_id>/', views.MypageEcoprogramApproveRejectView.as_view(), 
        name='mypage_ecoprogram_approve_rejection_view'), # 해당 에코프로그램 신청 인원 (조회, 처리)

    path('organization/<int:user_id>/upcyclings/', views.MypageUpcyclingCompanyManagementView.as_view(), 
        name='mypage_upcycling_company_management_view'), # 업사이클링 업체 등록 관리 (조회, 삭제)
]