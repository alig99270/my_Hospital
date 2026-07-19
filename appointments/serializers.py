from rest_framework import serializers
from .models import Appointment
from accounts.models import DoctorProfile, PatientProfile
from shifts.models import Shift


class AppointmentSerializer(serializers.ModelSerializer):
    patient_id = serializers.PrimaryKeyRelatedField(source='patient', queryset=PatientProfile.objects.all())
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=DoctorProfile.objects.all())
    shift_id = serializers.PrimaryKeyRelatedField(source='shift', queryset=Shift.objects.all(), required=False)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient_id', 'doctor_id', 'shift_id', 'start_time',
            'end_time', 'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        # Validate status transitions
        if 'status' in attrs:
            if self.instance:
                current_status = self.instance.status
                new_status = attrs['status']

                if current_status == 'booked' and new_status not in ['canceled', 'completed']:
                    raise serializers.ValidationError("Invalid status transition")
                if current_status in ['canceled', 'completed'] and new_status != current_status:
                    raise serializers.ValidationError("Cannot change status of completed/canceled appointment")

        return attrs