# traject/urls.py
from django.urls import path
from .views import create_trajet, start_trajet, end_trajet, pause_trajet, resume_trajet

urlpatterns = [
    path('trajets/', create_trajet, name='create_trajet'),
    path('trajets/<str:trajet_id>/start/', start_trajet, name='start_trajet'),
    path('trajets/<str:trajet_id>/end/', end_trajet, name='end_trajet'),
    path('trajets/<str:trajet_id>/pause/', pause_trajet, name='pause_trajet'),
    path('trajets/<str:trajet_id>/resume/', resume_trajet, name='resume_trajet'),
]
