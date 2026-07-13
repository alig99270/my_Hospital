from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta

from .models import Report, AppointmentStatistics, PatientStatistics, FinancialReport
from .serializers import (
    ReportSerializer,
    AppointmentStatisticsSerializer,
    PatientStatisticsSerializer,
    FinancialReportSerializer,
)
from accounts.models import User, DoctorProfile, PatientProfile
from appointments.models import Appointment
from medical_records.models import MedicalRecord


class ReportViewSet(viewsets.ModelViewSet):
    """ویوست برای مدیریت گزارش‌ها"""
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return Report.objects.all()
        return Report.objects.filter(generated_by=user)

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)

    @action(detail=False, methods=['get'])
    def daily_report(self, request):
        """گزارش روزانه"""
        today = timezone.now().date()
        appointments_count = Appointment.objects.filter(date=today).count()
        patients_count = PatientProfile.objects.count()
        doctors_count = DoctorProfile.objects.count()
        
        data = {
            'date': today,
            'appointments': appointments_count,
            'patients': patients_count,
            'doctors': doctors_count,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def monthly_report(self, request):
        """گزارش ماهانه"""
        now = timezone.now()
        start_of_month = now.replace(day=1)
        
        appointments = Appointment.objects.filter(date__gte=start_of_month).count()
        new_patients = PatientProfile.objects.filter(
            user__date_joined__gte=start_of_month
        ).count()
        
        data = {
            'month': start_of_month.strftime('%Y-%m'),
            'appointments': appointments,
            'new_patients': new_patients,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """آمار کلی سیستم"""
        total_users = User.objects.count()
        total_doctors = DoctorProfile.objects.count()
        total_patients = PatientProfile.objects.count()
        total_appointments = Appointment.objects.count()
        completed_appointments = Appointment.objects.filter(status='completed').count()
        
        data = {
            'total_users': total_users,
            'total_doctors': total_doctors,
            'total_patients': total_patients,
            'total_appointments': total_appointments,
            'completed_appointments': completed_appointments,
        }
        return Response(data)


class AppointmentStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ویوست برای آمار نوبت‌ها"""
    queryset = AppointmentStatistics.objects.all()
    serializer_class = AppointmentStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """خلاصه آمار نوبت‌ها"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        total = AppointmentStatistics.objects.filter(date__gte=week_ago).aggregate(
            total=Sum('total_appointments'),
            completed=Sum('completed_appointments'),
            cancelled=Sum('cancelled_appointments')
        )
        
        return Response(total)


class PatientStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """ویوست برای آمار بیماران"""
    queryset = PatientStatistics.objects.all()
    serializer_class = PatientStatisticsSerializer
    permission_classes = [permissions.IsAuthenticated]


class FinancialReportViewSet(viewsets.ModelViewSet):
    """ویوست برای گزارش‌های مالی"""
    queryset = FinancialReport.objects.all()
    serializer_class = FinancialReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return FinancialReport.objects.all()
        return FinancialReport.objects.none()
