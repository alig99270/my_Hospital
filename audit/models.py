from django.db import models
from accounts.models import User


OPERATION_CHOICES = [
    ('INSERT', 'Insert'),
    ('UPDATE', 'Update'),
    ('DELETE', 'Delete'),
]


class AuditLogManager(models.Manager):
    """Custom manager for AuditLog to simplify logging operations."""

    def log_operation(self, user, table_name, operation, record_id, change_details):
        """Create an audit log entry."""
        return self.create(
            user=user,
            table_name=table_name,
            operation=operation,
            record_id=record_id,
            change_details=change_details
        )


class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    table_name = models.CharField(max_length=100)
    operation = models.CharField(max_length=10, choices=OPERATION_CHOICES)
    record_id = models.PositiveIntegerField()
    changed_at = models.DateTimeField(auto_now_add=True)
    change_details = models.JSONField()

    objects = AuditLogManager()

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.operation} on {self.table_name} by {self.user.username}"