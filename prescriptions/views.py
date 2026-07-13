from rest_framework import viewsets
from .models import Prescription
from .serializers import PrescriptionSerializer
from hms.permissions import IsDoctor, IsAdmin


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsDoctor | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Prescription.objects.all()
        return Prescription.objects.filter(medical_record__doctor__user=self.request.user)