from rest_framework import viewsets
from .models import Appointment
from .serializers import AppointmentSerializer
from hms.permissions import IsDoctor, IsPatient, IsAdmin


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctor | IsPatient | IsAdmin]

    def get_queryset(self):
        user = self.request.user
        role_filters = {
            'Admin': Appointment.objects.all(),
            'Doctor': Appointment.objects.filter(doctor__user=user),
            'Patient': Appointment.objects.filter(patient__user=user),
        }
        return role_filters.get(user.role, Appointment.objects.none())