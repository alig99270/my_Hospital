from django.contrib import admin
from .models import Notification, SMSLog, NotificationTemplate


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'notification_type', 'priority', 'status', 'created_at']
    list_filter = ['notification_type', 'priority', 'status', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    ordering = ['-created_at']


@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'status', 'sent_at', 'provider', 'cost']
    list_filter = ['status', 'sent_at', 'provider']
    search_fields = ['recipient', 'message']
    ordering = ['-sent_at']


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'notification_type', 'is_active', 'created_at']
    list_filter = ['notification_type', 'is_active']
    search_fields = ['name', 'subject']
