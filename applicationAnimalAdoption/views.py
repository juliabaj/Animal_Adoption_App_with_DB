from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Owners, User, Animals, HealthRecords, Admins
from .serializers import OwnersSerializer, UserSerializer, AnimalsSerializer, HealthRecordsSerializer, AdminsSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class OwnersView(generics.ListAPIView):
    queryset = Owners.objects.all()
    serializer_class = OwnersSerializer

    def get_queryset(self):
        return Owners.objects.all()


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()


class AnimalsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        animals = Animals.objects.all()
        serializer = AnimalsSerializer(animals, many=True)
        return Response(serializer.data)


class HealthRecordsView(generics.ListAPIView):
    queryset = HealthRecords.objects.all()
    serializer_class = HealthRecordsSerializer

    def get_queryset(self):
        return HealthRecords.objects.filter(chipped=True)


class AdminsView(generics.ListAPIView):
    queryset = Admins.objects.all()
    serializer_class = AdminsSerializer

    def get_queryset(self):
        return Admins.objects.all()


class AdoptionAnimalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, animal_id):
        try:
            # Znalezienie zwierzęcia według ID
            animal = Animals.objects.get(animal_id=animal_id)
            if animal.adoption_status != 'available':
                return Response({"detail": "Animal not available for adoption."}, status=status.HTTP_400_BAD_REQUEST)

            # Zmiana statusu adopcji
            animal.adoption_status = 'pending'  # Możesz dodać status 'pending', zanim admin zatwierdzi adopcję
            animal.save()

            return Response({"detail": "Animal adoption request submitted successfully."}, status=status.HTTP_200_OK)

        except Animals.DoesNotExist:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

class UpdateOwnerStatusView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, owner_id):
        owner = Owners.objects.get(id=owner_id)
        new_status = request.data.get("status")

        # Check if the new status is valid
        if new_status not in ["unverified", "in_progress", "verified"]:
            return Response({"detail": "Invalid status."}, status=400)

        owner.is_verified = new_status
        owner.save()

        # If verified, assign the owner to the animal
        if new_status == "verified":
            owner.animal.owner = owner
            owner.animal.save()

        return Response({"detail": "Owner status updated."}, status=200)
