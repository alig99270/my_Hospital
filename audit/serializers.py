from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id', 'user_id', 'table_name', 'operation',
            'record_id', 'changed_at', 'change_details'
        ]
        read_only_fields = ['id']