# medical_records/serializers.py
from rest_framework import serializers
from .models import MedicalRecord
from accounts.models import DoctorProfile, PatientProfile


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=PatientProfile.objects.all())
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=DoctorProfile.objects.all())

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient_id', 'doctor_id', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']


