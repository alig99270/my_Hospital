from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import DoctorProfile, PatientProfile

User = get_user_model()


class Report(models.Model):
    """مدل برای گزارش‌های سیستم"""
    REPORT_TYPES = [
        ('daily', 'گزارش روزانه'),
        ('weekly', 'گزارش هفتگی'),
        ('monthly', 'گزارش ماهانه'),
        ('yearly', 'گزارش سالانه'),
        ('custom', 'گزارش سفارشی'),
    ]

    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق'),
    ]

    title = models.CharField(max_length=200, verbose_name='عنوان گزارش')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES, verbose_name='نوع گزارش')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', verbose_name='تولید کننده')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='وضعیت')
    file_path = models.CharField(max_length=500, blank=True, null=True, verbose_name='مسیر فایل')
    parameters = models.JSONField(default=dict, blank=True, verbose_name='پارامترها')

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = 'گزارش‌ها'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.created_at}"


class AppointmentStatistics(models.Model):
    """آمار نوبت‌ها"""
    date = models.DateField(verbose_name='تاریخ')
    total_appointments = models.IntegerField(default=0, verbose_name='کل نوبت‌ها')
    completed_appointments = models.IntegerField(default=0, verbose_name='نوبت‌های تکمیل شده')
    cancelled_appointments = models.IntegerField(default=0, verbose_name='نوبت‌های لغو شده')
    no_show_appointments = models.IntegerField(default=0, verbose_name='نوبت‌های عدم حضور')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='statistics', verbose_name='پزشک', null=True, blank=True)

    class Meta:
        verbose_name = 'آمار نوبت'
        verbose_name_plural = 'آمار نوبت‌ها'
        ordering = ['-date']

    def __str__(self):
        return f"آمار {self.date} - کل: {self.total_appointments}"


class PatientStatistics(models.Model):
    """آمار بیماران"""
    date = models.DateField(verbose_name='تاریخ')
    total_patients = models.IntegerField(default=0, verbose_name='کل بیماران')
    new_patients = models.IntegerField(default=0, verbose_name='بیماران جدید')
    active_patients = models.IntegerField(default=0, verbose_name='بیماران فعال')

    class Meta:
        verbose_name = 'آمار بیمار'
        verbose_name_plural = 'آمار بیماران'
        ordering = ['-date']

    def __str__(self):
        return f"آمار بیماران {self.date}"


class FinancialReport(models.Model):
    """گزارش مالی"""
    date = models.DateField(verbose_name='تاریخ')
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='درآمد کل')
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='هزینه کل')
    net_profit = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='سود خالص')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'گزارش مالی'
        verbose_name_plural = 'گزارش‌های مالی'
        ordering = ['-date']

    def __str__(self):
        return f"گزارش مالی {self.date}"

# Create your models here.
