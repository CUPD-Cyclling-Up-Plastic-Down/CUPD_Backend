from django.urls import path
from upcyclings import views

urlpatterns = [
    path('',),
    path('<int:upcycling_id>/',),
    path('enroll/',),
]