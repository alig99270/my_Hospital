from rest_framework import viewsets
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from hms.permissions import IsDoctor, IsAdmin


class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsDoctor | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return MedicalRecord.objects.all()
        return MedicalRecord.objects.filter(doctor__user=self.request.user)

