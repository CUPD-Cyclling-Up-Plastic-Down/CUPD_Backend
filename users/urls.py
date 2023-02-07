from django.urls import path
from users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
) 


urlpatterns = [
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'), # access token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # refresh token
    path('signup/', views.SignUpView.as_view(), name='signup_view'),

    # path('kakao/callback/'),
    # path('google/callback/'),
    # path('con/<int:user_id>/'),
    # path('con/<int:user_id>/apply/'),
    # path('con/<int:user_id>/approve/'),
    # path('con/<int:user_id>/likes/'),
    # path('org/<int:user_id>/'),
    # path('org/<int:user_id>/make/'),
    # path('org/<int:user_id>/make/<int:ecoprogram_id>/'),
    # path('org/<int:user_id>/upcyclings/'),
]