from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import CustomUser, Room

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class ResidentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'student_id', 'move_in_date', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class RoomAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['number', 'capacity', 'occupants']

    def update(self, instance, validated_data):
        if instance.is_full():
            raise serializers.ValidationError("Room is already full.")
        return super().update(instance, validated_data)