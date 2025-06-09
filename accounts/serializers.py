from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, StaffProfile, PatientProfile
from hms.utils import user_profile_factory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        read_only_fields = ['id']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['user', 'specialization', 'department']
        read_only_fields = ['user']


class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StaffProfile
        fields = ['user', 'position']
        read_only_fields = ['user']


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            'user', 'full_name', 'date_of_birth', 'gender',
            'email', 'phone', 'profile_photo', 'medical_history_summary'
        ]
        read_only_fields = ['user']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    profile_data = serializers.JSONField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'profile_data']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile_data')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role']
        )

        # Use Factory Method Pattern to create appropriate profile
        profile = user_profile_factory.create_profile(user, profile_data)
        return user