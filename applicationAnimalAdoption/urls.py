from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views  # Importuje widoki z pliku views.py

# Tworzymy router i rejestrujemy widoki
router = DefaultRouter()
router.register(r'owners', views.OwnersViewSet)
router.register(r'users', views.UsersViewSet)
router.register(r'animals', views.AnimalsViewSet)
router.register(r'healthrecords', views.HealthRecordsViewSet)
router.register(r'admins', views.AdminsViewSet)


urlpatterns = [
    path('', views.all_user)
]
