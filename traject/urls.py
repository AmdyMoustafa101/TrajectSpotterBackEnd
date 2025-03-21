from django.urls import path
from .views import (
    create_trip, start_trip, end_trip,
    start_sleep, end_sleep, start_onduty, end_onduty,
    start_offduty, end_offduty, get_resume
)

urlpatterns = [
    path('trips/', create_trip, name='create_trip'),
    path('trips/<str:trip_id>/start/', start_trip, name='start_trip'),
    path('trips/<str:trip_id>/end/', end_trip, name='end_trip'),
    path('trips/<str:trip_id>/start-sleep/', start_sleep, name='start_sleep'),
    path('trips/<str:trip_id>/end-sleep/', end_sleep, name='end_sleep'),
    path('trips/<str:trip_id>/start-onduty/', start_onduty, name='start_onduty'),
    path('trips/<str:trip_id>/end-onduty/', end_onduty, name='end_onduty'),
    path('trips/<str:trip_id>/start-offduty/', start_offduty, name='start_offduty'),
    path('trips/<str:trip_id>/end-offduty/', end_offduty, name='end_offduty'),
    path('trips/<str:trip_id>/resume/', get_resume, name='get_resume'),
]