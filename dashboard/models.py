from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, PatientProfile

User = get_user_model()


class DashboardWidget(models.Model):
    """مدل برای ویجت‌های داشبورد"""
    WIDGET_TYPES = [
        ('statistics', 'آمار'),
        ('chart', 'نمودار'),
        ('table', 'جدول'),
        ('calendar', 'تقویم'),
        ('alerts', 'هشدارها'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام ویجت')
    widget_type = models.CharField(max_length=20, choices=WIDGET_TYPES, verbose_name='نوع ویجت')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    configuration = models.JSONField(default=dict, blank=True, verbose_name='پیکربندی')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    order = models.IntegerField(default=0, verbose_name='ترتیب نمایش')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'ویجت داشبورد'
        verbose_name_plural = 'ویجت‌های داشبورد'
        ordering = ['order']

    def __str__(self):
        return self.name


class DashboardMetric(models.Model):
    """مدل برای معیارهای داشبورد مدیریتی"""
    METRIC_TYPES = [
        ('appointments', 'نوبت‌ها'),
        ('patients', 'بیماران'),
        ('doctors', 'پزشکان'),
        ('revenue', 'درآمد'),
        ('prescriptions', 'نسخه‌ها'),
    ]

    name = models.CharField(max_length=100, verbose_name='نام معیار')
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES, verbose_name='نوع معیار')
    value = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='مقدار')
    change_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name='درصد تغییر')
    date = models.DateField(verbose_name='تاریخ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'معیار داشبورد'
        verbose_name_plural = 'معیارهای داشبورد'
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} - {self.date}"


class PatientDashboard(models.Model):
    """داشبورد اختصاصی بیمار"""
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name='dashboard', verbose_name='بیمار')
    last_visit = models.DateTimeField(null=True, blank=True, verbose_name='آخرین مراجعه')
    next_appointment = models.DateTimeField(null=True, blank=True, verbose_name='نوبت بعدی')
    pending_prescriptions = models.IntegerField(default=0, verbose_name='نسخه‌های در انتظار')
    unread_notifications = models.IntegerField(default=0, verbose_name='نوتیفیکیشن‌های خوانده نشده')
    health_score = models.IntegerField(default=0, verbose_name='امتیاز سلامت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'داشبورد بیمار'
        verbose_name_plural = 'داشبوردهای بیماران'

    def __str__(self):
        return f"داشبورد {self.patient.full_name}"


class AdminDashboardSettings(models.Model):
    """تنظیمات داشبورد مدیریتی"""
    refresh_interval = models.IntegerField(default=300, verbose_name='فاصله به‌روزرسانی (ثانیه)')
    show_real_time_stats = models.BooleanField(default=True, verbose_name='نمایش آمار لحظه‌ای')
    default_date_range = models.IntegerField(default=30, verbose_name='بازه پیش‌فرض (روز)')
    max_records_per_page = models.IntegerField(default=20, verbose_name='حداکثر رکورد در صفحه')
    enable_export = models.BooleanField(default=True, verbose_name='فعال کردن خروجی')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')

    class Meta:
        verbose_name = 'تنظیمات داشبورد'
        verbose_name_plural = 'تنظیمات داشبورد'

    def __str__(self):
        return "تنظیمات داشبورد مدیریتی"

# Create your models here.
