from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from audit.models import AuditLog
from django.apps import apps
import json

@receiver(post_save)
def log_post_save(sender, instance, created, **kwargs):
    if not issubclass(sender, AuditLog):  # Prevent infinite recursion
        user = getattr(instance, 'modified_by', None) or getattr(instance, 'created_by', None)
        if user and hasattr(user, 'id'):
            table_name = sender._meta.db_table
            data = {
                'id': getattr(instance, 'id', None),
                **{field.name: getattr(instance, field.name) for field in sender._meta.get_fields()}
            }
            AuditLog.objects.create(
                user=user,
                table_name=table_name,
                operation='INSERT' if created else 'UPDATE',
                record_id=instance.id,
                change_details=json.dumps(data)
            )

@receiver(post_delete)
def log_post_delete(sender, instance, **kwargs):
    if not issubclass(sender, AuditLog):
        user = getattr(instance, 'modified_by', None) or getattr(instance, 'created_by', None)
        if user and hasattr(user, 'id'):
            table_name = sender._meta.db_table
            data = {
                'id': getattr(instance, 'id', None),
                **{field.name: getattr(instance, field.name) for field in sender._meta.get_fields()}
            }
            AuditLog.objects.create(
                user=user,
                table_name=table_name,
                operation='DELETE',
                record_id=instance.id,
                change_details=json.dumps(data)
            )