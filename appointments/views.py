from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.models import DoctorProfile, PatientProfile
from hms.permissions import IsDoctor, IsPatient, IsAdmin

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctor | IsPatient | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Appointment.objects.all()
        elif user.role == 'Doctor':
            return Appointment.objects.filter(doctor__user=user)
        elif user.role == 'Patient':
            return Appointment.objects.filter(patient__user=user)
        return Appointment.objects.none()