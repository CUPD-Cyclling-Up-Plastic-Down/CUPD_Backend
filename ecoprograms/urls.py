from django.urls import path
from ecoprograms import views

urlpatterns = [
    path('',),
    path('<int:ecoprogram_id>/',),
    path('<int:ecoprogram_id>/like/',),
    path('enroll/',),
]