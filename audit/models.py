from django.db import models
from accounts.models import User
import json

class AuditLog(models.Model):
    OPERATION_CHOICES = [
        ('INSERT', 'Insert'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    table_name = models.CharField(max_length=100)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    record_id = models.PositiveIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)
    change_details = models.JSONField()

    def __str__(self):
        return f"{self.operation} on {self.table_name} by {self.user.username}"