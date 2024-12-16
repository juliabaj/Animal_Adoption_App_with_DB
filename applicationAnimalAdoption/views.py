from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Owners, Users, Animals, HealthRecords
from .serializers import OwnersSerializer, UsersSerializer, AnimalsSerializer, HealthRecordsSerializer

def all_user(request):
    return HttpResponse('Return all users')

class OwnersViewSet(viewsets.ModelViewSet):
    queryset = Owners.objects.all()
    serializer_class = OwnersSerializer

    def get_queryset(self):
        return Owners.objects.all()

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_queryset(self):
        return Users.objects.all()

class AnimalsViewSet(viewsets.ModelViewSet):
    queryset = Animals.objects.all()
    serializer_class = AnimalsSerializer

    def get_queryset(self):
        return Animals.objects.all()

class HealthRecordsViewSet(viewsets.ModelViewSet):
    queryset = HealthRecords.objects.all()
    serializer_class = HealthRecordsSerializer

    def get_queryset(self):
        return HealthRecords.objects.filter(chipped=True)

