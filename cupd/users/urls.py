from django.urls import path
from users import views


urlpatterns = [
    path('api/token/', ),
    path('api/token/refresh/', ),
    path('kakao/callback/'),
    path('google/callback/'),
    path('signup/', ),
    path('con/<int:user_id>/'),
    path('con/<int:user_id>/apply/'),
    path('con/<int:user_id>/approve/'),
    path('con/<int:user_id>/likes/'),
    path('org/<int:user_id>/'),
    path('org/<int:user_id>/make/'),
    path('org/<int:user_id>/make/<int:ecoprogram_id>/'),
    path('org/<int:user_id>/upcyclings/'),
]