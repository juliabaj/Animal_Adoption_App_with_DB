from django.contrib import admin
from django.urls import path, include
from applicationAnimalAdoption.views import CreateUserView, AnimalsListView, AdoptionAnimalView, UpdateOwnerStatusView, SqlInjectionDemoView, HealthRecordsView, SqlInjectionSearchBar
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applicationAnimalAdoption import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name="register"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth", include("rest_framework.urls")),
    path('api/', include("applicationAnimalAdoption.urls")),
    path('api/animals/', AnimalsListView.as_view(), name='animals-list'),
    path('vulnerable', SqlInjectionDemoView.as_view(), name='vulnerable-view'),
    path('animals/<int:animal_id>/', HealthRecordsView.as_view(), name='animal-detail'),
    path('animals/<int:animal_id>/healthrecords/', HealthRecordsView.as_view(), name='animal-healthrecords'),
    path("api/sql/", SqlInjectionSearchBar.as_view(), name="sql_injection_demo"),
    ]
