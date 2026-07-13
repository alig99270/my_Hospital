from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    """مدل برای نوتیفیکیشن‌ها و پیامک‌ها"""
    NOTIFICATION_TYPES = [
        ('sms', 'پیامک'),
        ('email', 'ایمیل'),
        ('push', 'نوتیفیکیشن پوش'),
        ('in_app', 'نوتیفیکیشن داخلی'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'کم'),
        ('medium', 'متوسط'),
        ('high', 'بالا'),
        ('urgent', 'فوری'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('sent', 'ارسال شده'),
        ('failed', 'ناموفق'),
        ('read', 'خوانده شده'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name='کاربر', null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='عنوان')
    message = models.TextField(verbose_name='پیام')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='in_app', verbose_name='نوع نوتیفیکیشن')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium', verbose_name='اولویت')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارسال')
    read_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ خواندن')
    recipient_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='شماره موبایل گیرنده')
    recipient_email = models.EmailField(blank=True, null=True, verbose_name='ایمیل گیرنده')
    metadata = models.JSONField(default=dict, blank=True, verbose_name='داده‌های اضافی')

    class Meta:
        verbose_name = 'نوتیفیکیشن'
        verbose_name_plural = 'نوتیفیکیشن‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username if self.user else 'عمومی'}"


class SMSLog(models.Model):
    """لاگ پیامک‌های ارسالی"""
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('sent', 'ارسال شده'),
        ('failed', 'ناموفق'),
    ]

    recipient = models.CharField(max_length=20, verbose_name='شماره گیرنده')
    message = models.TextField(verbose_name='متن پیامک')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ ارسال')
    error_message = models.TextField(blank=True, null=True, verbose_name='پیام خطا')
    provider = models.CharField(max_length=50, default='default', verbose_name='ارائه دهنده')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='هزینه')

    class Meta:
        verbose_name = 'لاگ پیامک'
        verbose_name_plural = 'لاگ پیامک‌ها'
        ordering = ['-sent_at']

    def __str__(self):
        return f"SMS به {self.recipient} - {self.status}"


class NotificationTemplate(models.Model):
    """قالب‌های نوتیفیکیشن"""
    name = models.CharField(max_length=100, verbose_name='نام قالب')
    subject = models.CharField(max_length=200, verbose_name='موضوع')
    body = models.TextField(verbose_name='متن قالب')
    notification_type = models.CharField(max_length=20, choices=Notification.NOTIFICATION_TYPES, verbose_name='نوع نوتیفیکیشن')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'قالب نوتیفیکیشن'
        verbose_name_plural = 'قالب‌های نوتیفیکیشن'

    def __str__(self):
        return self.name

# Create your models here.
