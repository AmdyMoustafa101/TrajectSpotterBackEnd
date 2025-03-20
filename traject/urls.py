from django.urls import path
from .views import (
    create_trajet, start_trajet, end_trajet,
    start_sleep, end_sleep, start_onduty, end_onduty,
    start_offduty, end_offduty
)

urlpatterns = [
    path('trajets/', create_trajet, name='create_trajet'),
    path('trajets/<str:trajet_id>/start/', start_trajet, name='start_trajet'),
    path('trajets/<str:trajet_id>/end/', end_trajet, name='end_trajet'),
    path('trajets/<str:trajet_id>/start-sleep/', start_sleep, name='start_sleep'),
    path('trajets/<str:trajet_id>/end-sleep/', end_sleep, name='end_sleep'),
    path('trajets/<str:trajet_id>/start-onduty/', start_onduty, name='start_onduty'),
    path('trajets/<str:trajet_id>/end-onduty/', end_onduty, name='end_onduty'),
    path('trajets/<str:trajet_id>/start-offduty/', start_offduty, name='start_offduty'),
    path('trajets/<str:trajet_id>/end-offduty/', end_offduty, name='end_offduty'),
]