from django.urls import path
from ecoprograms import views

urlpatterns = [
    path('<int:ecoprogram_id>/review/', views.EcoprogramReviewView.as_view(), 
        name='ecoprogram_review_view'), # 리뷰 전체보기 및 등록

    path('<int:ecoprogram_id>/review/<int:review_id>', views.EcoprogramReviewDetailView.as_view(), 
        name='ecoprogram_review_detail_view'), # 작성한 리뷰 수정 및 삭제

    path('', views.EcoproramView.as_view(), 
        name='ecoprogram_view'), # 전체 프로그램 조회
    
    path('<int:ecoprogram_id>/', views.EcoprogramDetailView.as_view(), 
        name='ecoprogram_detail_view'), # 해당 프로그램 상세 페이지 (조회, 수정, 삭제)

    path('<int:ecoprogram_id>/like/', views.EcoprogramDetailLikeView.as_view(), 
        name='ecoprogram_detail_like_view'), # 해당 에코프로그램 '좋아요'

    path('<int:ecoprogram_id>/apply/', views.EcoprogramDetailApplyView.as_view(), 
        name='ecoprogram_detail_apply_view'), # 해당 프로그램 상세 페이지에서 '신청'

    path('enroll/', views.EcoprogramEnrollView.as_view(), 
        name='ecoprogram_enroll_view'), # 프로그램 추가 등록
        
    # path('lank/') # 프로그램 정렬 (인기순, 최신순)
]