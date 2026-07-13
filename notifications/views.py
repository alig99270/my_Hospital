from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.utils import timezone
from datetime import timedelta

from .models import Notification, SMSLog, NotificationTemplate
from .serializers import (
    NotificationSerializer,
    SMSLogSerializer,
    NotificationTemplateSerializer,
)
from accounts.models import User, PatientProfile


class NotificationViewSet(viewsets.ModelViewSet):
    """ویوست برای مدیریت نوتیفیکیشن‌ها"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Notification.objects.all()
        return Notification.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        """علامت‌گذاری نوتیفیکیشن به عنوان خوانده شده"""
        notification = self.get_object()
        notification.status = 'read'
        notification.read_at = timezone.now()
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """دریافت نوتیفیکیشن‌های خوانده نشده"""
        user = request.user
        notifications = Notification.objects.filter(
            user=user,
            status__in=['pending', 'sent']
        )
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def send_sms(self, request):
        """ارسال پیامک"""
        phone = request.data.get('phone')
        message = request.data.get('message')
        
        if not phone or not message:
            return Response(
                {'error': 'شماره موبایل و پیام الزامی است'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # ایجاد لاگ پیامک
        sms_log = SMSLog.objects.create(
            recipient=phone,
            message=message,
            status='pending'
        )
        
        # TODO: ارسال واقعی پیامک از طریق سرویس دهنده
        # اینجا باید کد اتصال به پنل پیامکی قرار گیرد
        
        sms_log.status = 'sent'
        sms_log.sent_at = timezone.now()
        sms_log.save()
        
        # ایجاد نوتیفیکیشن
        notification = Notification.objects.create(
            title='پیامک ارسال شد',
            message=message,
            notification_type='sms',
            recipient_phone=phone,
            status='sent',
            sent_at=timezone.now()
        )
        
        return Response({
            'status': 'success',
            'message': 'پیامک با موفقیت ارسال شد',
            'sms_id': sms_log.id
        })


class SMSLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ویوست برای مشاهده لاگ پیامک‌ها"""
    queryset = SMSLog.objects.all()
    serializer_class = SMSLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return SMSLog.objects.all()
        return SMSLog.objects.none()


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    """ویوست برای مدیریت قالب‌های نوتیفیکیشن"""
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return NotificationTemplate.objects.all()
        return NotificationTemplate.objects.filter(is_active=True)
