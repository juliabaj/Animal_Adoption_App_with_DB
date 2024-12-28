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

import logging
logger = logging.getLogger(__name__)

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
            # Pobierz zwierzę
            animal = Animals.objects.get(animal_id=animal_id)

            # Obsługa różnych statusów adopcji
            if animal.adoption_status == 'pending':
                # Sprawdź, czy użytkownik już zgłosił adopcję
                owner_exists = Owners.objects.filter(user=request.user, animal=animal).exists()
                if owner_exists:
                    return Response({"detail": "You have already requested adoption of this animal."},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": "This animal is already pending adoption by another user."},
                                status=status.HTTP_400_BAD_REQUEST)

            if animal.adoption_status == 'adopted':
                return Response({"detail": "This animal has already been adopted."}, status=status.HTTP_400_BAD_REQUEST)

            # Zmień status na 'pending'
            animal.adoption_status = 'pending'
            animal.save()

            # Tworzenie lub pobranie właściciela
            owner, created = Owners.objects.get_or_create(
                user=request.user,
                defaults={
                    'owner_name': request.user.username,
                    'email': request.user.email,
                    'address': 'Default Address',
                    'phone_number': '123456789',
                    'is_verified': 'in_progress',
                }
            )

            return Response({"detail": "Animal adoption request submitted successfully."}, status=status.HTTP_200_OK)

        except Animals.DoesNotExist:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"detail": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UpdateOwnerStatusView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, owner_id):
        owner = Owners.objects.get(owner_id=owner_id)
        new_status = request.data.get("status")

        # Check if the new status is valid
        if new_status not in ["unverified", "in_progress", "verified"]:
            return Response({"detail": "Invalid status."}, status=400)

        owner.is_verified = new_status
        owner.save()

        # If verified, assign the owner to the animal
        if new_status == "verified":
            animal = owner.animal or Animals.objects.filter(adoption_status='pending', owner__isnull=True).first()
            if animal:
                animal.set_adopted(owner)

        return Response({"detail": "Owner status updated."}, status=200)



# class TestOwnerCreationView(APIView):
#     def get(self, request):
#         from applicationAnimalAdoption.models import Owners, User
#
#         user = User.objects.first()  # Pobierz pierwszego użytkownika
#         owner = Owners.objects.create(
#             user=user,
#             owner_name="Test Owner",
#             email="testowner@example.com",
#             address="Test Address",
#             phone_number="123456789",
#             is_verified="in_progress"
#         )
#         return Response({"detail": f"Owner created: {owner}"}, status=status.HTTP_201_CREATED)