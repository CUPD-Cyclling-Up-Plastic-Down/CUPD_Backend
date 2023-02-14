from django.urls import path
from upcyclings import views

urlpatterns = [
    path('', views.UpcyclingCompanyListView.as_view(), 
        name='upcycling_company_list_view'), # 전체 업사이클링 업체 리스트 조회

    path('<int:upcycling_id>/', views.UpcyclingCompanyDetailView.as_view(), 
        name='upcycling_company_detail_view'), # 해당 업사이클링 업체 상세 페이지 (조회, 수정, 삭제)

    path('enroll/', views.UpcyclingCompanyEnrollView.as_view(), 
        name='upcycling_company_enroll_view'), # 업사이클링 업체 추가 등록
]