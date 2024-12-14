from rest_framework import serializers
from .models import Owners, Users, Animals, HealthRecords

class OwnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owners
        fields = '__all__'     # All fields will be serialized

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class AnimalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animals
        fields = '__all__'

class HealthRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthRecords
        fields = '__all__'