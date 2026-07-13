from rest_framework import viewsets
from .models import Shift
from .serializers import ShiftSerializer
from hms.permissions import IsDoctor, IsAdmin


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all()
    serializer_class = ShiftSerializer
    permission_classes = [IsDoctor | IsAdmin]

    def get_queryset(self):
        if self.request.user.role == 'Admin':
            return Shift.objects.all()
        return Shift.objects.filter(doctor__user=self.request.user)