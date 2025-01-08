from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views  # Importuje widoki z pliku views.py
from .views import OwnersView, AnimalsListView, HealthRecordsView, AdoptionAnimalView, UpdateOwnerStatusView, SqlInjectionDemoView, HealthRecordsView, SqlInjectionSearchBar

urlpatterns = [
    path('owners/', views.OwnersView.as_view(), name='owners-list'),
    path('api/animals/', AnimalsListView.as_view(), name='animals-list'),
    path('health-records/', HealthRecordsView.as_view(), name='health-records-list'),
    path('animals/adopt/<int:animal_id>/', AdoptionAnimalView.as_view(), name='adopt-animal'),
    path('owners/update-status/<int:owner_id>/', UpdateOwnerStatusView.as_view(), name='update-owner-status'),
    path('vulnerable', SqlInjectionDemoView.as_view(), name='vulnerable-view'),
    path('animals/<int:animal_id>/healthrecords/', HealthRecordsView.as_view(), name='animal-healthrecords'),
    path("api/sql/", SqlInjectionSearchBar.as_view(), name="sql_injection_demo"),
]
