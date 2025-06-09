# prescriptions/serializers.py
from rest_framework import serializers
from .models import Prescription
from medical_records.models import MedicalRecord


class PrescriptionSerializer(serializers.ModelSerializer):
    medical_record_id = serializers.PrimaryKeyRelatedField(source='medical_record',
                                                           queryset=MedicalRecord.objects.all())

    class Meta:
        model = Prescription
        fields = [
            'id', 'medical_record_id', 'medicine_name', 'dosage',
            'frequency', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']