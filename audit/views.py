from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
from hms.permissions import IsAdmin

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdmin]