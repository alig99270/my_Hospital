from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Shift
from .serializers import ShiftSerializer
from accounts.models import DoctorProfile
from hms.permissions import IsDoctor, IsAdmin

class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsDoctor | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Shift.objects.all()
        return Shift.objects.filter(doctor__user=self.request.user)