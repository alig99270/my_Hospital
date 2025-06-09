from rest_framework import serializers
from .models import Shift
from accounts.models import DoctorProfile


class ShiftSerializer(serializers.ModelSerializer):
    doctor_id = serializers.PrimaryKeyRelatedField(source='doctor', queryset=DoctorProfile.objects.all(),
                                                   write_only=True)

    class Meta:
        model = Shift
        fields = ['id', 'doctor_id', 'start_time', 'end_time', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        start_time = attrs.get('start_time')
        end_time = attrs.get('end_time')

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time")

        return attrs