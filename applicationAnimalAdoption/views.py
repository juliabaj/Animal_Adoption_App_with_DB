from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Owners, Users, Animals, HealthRecords, Admins
from .serializers import OwnersSerializer, UsersSerializer, AnimalsSerializer, HealthRecordsSerializer, AdminsSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

def home(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'home.html', {})

def logout_user(request):
    pass


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

class AdminsViewSet(viewsets.ModelViewSet):
    queryset = Admins.objects.all()
    serializer_class = AdminsSerializer

    def get_queryset(self):
        return Admins.objects.all()
