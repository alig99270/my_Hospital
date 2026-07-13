from django.contrib import admin
from .models import Report, AppointmentStatistics, PatientStatistics, FinancialReport


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'report_type', 'status', 'generated_by', 'created_at']
    list_filter = ['report_type', 'status', 'created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']


@admin.register(AppointmentStatistics)
class AppointmentStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_appointments', 'completed_appointments', 'cancelled_appointments', 'doctor']
    list_filter = ['date', 'doctor']
    ordering = ['-date']


@admin.register(PatientStatistics)
class PatientStatisticsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_patients', 'new_patients', 'active_patients']
    list_filter = ['date']
    ordering = ['-date']


@admin.register(FinancialReport)
class FinancialReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_revenue', 'total_expenses', 'net_profit']
    list_filter = ['date']
    ordering = ['-date']
