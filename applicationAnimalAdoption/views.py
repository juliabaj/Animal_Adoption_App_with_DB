from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from django.db import connection
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
        return Response(serializer.data, status=status.HTTP_200_OK)


class HealthRecordsView(APIView):
    def get(self, request, animal_id):
        try:
            animal = Animals.objects.get(animal_id=animal_id)
            health_records = HealthRecords.objects.filter(animal_id=animal)

            animal_data = {
                "animal_id": animal.animal_id,
                "animal_name": animal.animal_name,
            }

            serializer = HealthRecordsSerializer(health_records, many=True)

            return Response({
                "animal": animal_data,
                "health_records": serializer.data
            }, status=status.HTTP_200_OK)

        except Animals.DoesNotExist:
            return Response({"detail": "Animal not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminsView(generics.ListAPIView):
    queryset = Admins.objects.all()
    serializer_class = AdminsSerializer

    def get_queryset(self):
        return Admins.objects.all()


class AdoptionAnimalView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, animal_id):
        try:
            # Pobieranie zwierzęcia
            animal = Animals.objects.get(animal_id=animal_id)

            # różne statusy adopcji
            if animal.adoption_status == 'pending':
                # Sprawdzenie, czy użytkownik już zgłosił adopcję
                owner_exists = Owners.objects.filter(user=request.user, animal=animal).exists()
                if owner_exists:
                    return Response({"detail": "You have already requested adoption of this animal."},
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response({"detail": "This animal is already pending adoption by another user."},
                                status=status.HTTP_400_BAD_REQUEST)

            if animal.adoption_status == 'adopted':
                return Response({"detail": "This animal has already been adopted."}, status=status.HTTP_400_BAD_REQUEST)

            # Zmiana statusu na 'pending'
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


class SqlInjectionDemoView(APIView):
    def get(self, request):
        owner_id = request.GET.get("owner_id", "")  # Pobranie parametru owner_id z URL

        query = f"SELECT * FROM applicationanimaladoption_owners WHERE owner_id = {owner_id}"  # Wstawienie parametru bezpośrednio do SQL query

        with connection.cursor() as cursor:
            cursor.execute(query)  # Wykonanie zapytania
            results = cursor.fetchall()

        return Response(results)


class SqlInjectionSearchBar(APIView):
    def get(self, request):
        # Pobranie zapytania SQL z parametru `query`
        raw_query = request.GET.get("query", "")

        if not raw_query:
            return Response({"error": "No query provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Wykonanie surowego zapytania SQL (niezabezpieczonego!)
            with connection.cursor() as cursor:
                cursor.execute(raw_query)
                results = cursor.fetchall()
                columns = [col[0] for col in cursor.description]
                formatted_results = [dict(zip(columns, row)) for row in results]

            return Response({"results": formatted_results}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
