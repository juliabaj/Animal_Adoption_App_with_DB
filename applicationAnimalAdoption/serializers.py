from rest_framework import serializers
from .models import Owners, Animals, HealthRecords, Admins
from django.contrib.auth.models import User


class OwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = ['owner_id', 'owner_name', 'user', 'address' 'phone_number', 'email',
                  'is_verified']  # All fields will be serialized


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AnimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = ['animal_id', 'animal_name', 'birth_date', 'species', 'gender', 'owner', 'adoption_status']


class HealthRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecords
        fields = ['animal_id', 'diagnosis', 'veterinarian', 'treatment', 'chipped', 'vaccinated']


class AdminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admins
        fields = ['admin_id', 'username', 'passwd']


