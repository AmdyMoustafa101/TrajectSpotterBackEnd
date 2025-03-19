# traject/urls.py
from django.urls import path
from .views import create_trajet

urlpatterns = [
    path('trajets/', create_trajet, name='create_trajet'),  # URL pour créer un trajet
]