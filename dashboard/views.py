from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone
from datetime import timedelta

from .models import DashboardWidget, DashboardMetric, PatientDashboard, AdminDashboardSettings
from .serializers import (
    DashboardWidgetSerializer,
    DashboardMetricSerializer,
    PatientDashboardSerializer,
    AdminDashboardSettingsSerializer,
)
from accounts.models import User, DoctorProfile, PatientProfile
from appointments.models import Appointment
from medical_records.models import MedicalRecord
from prescriptions.models import Prescription


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """ویوست برای مدیریت ویجت‌های داشبورد"""
    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return DashboardWidget.objects.filter(is_active=True)
        return DashboardWidget.objects.filter(is_active=True)


class DashboardMetricViewSet(viewsets.ReadOnlyModelViewSet):
    """ویوست برای معیارهای داشبورد"""
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """خلاصه معیارهای داشبورد"""
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        
        # آمار نوبت‌ها
        total_appointments = Appointment.objects.count()
        today_appointments = Appointment.objects.filter(date=today).count()
        week_appointments = Appointment.objects.filter(date__gte=week_ago).count()
        
        # آمار بیماران
        total_patients = PatientProfile.objects.count()
        
        # آمار پزشکان
        total_doctors = DoctorProfile.objects.count()
        
        # آمار نسخه‌ها
        total_prescriptions = Prescription.objects.count() if Prescription else 0
        
        data = {
            'total_appointments': total_appointments,
            'today_appointments': today_appointments,
            'week_appointments': week_appointments,
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_prescriptions': total_prescriptions,
        }
        return Response(data)


class PatientDashboardViewSet(viewsets.ModelViewSet):
    """ویوست برای داشبورد بیمار"""
    queryset = PatientDashboard.objects.all()
    serializer_class = PatientDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Patient':
            return PatientDashboard.objects.filter(patient=user.patientprofile)
        elif user.role == 'Admin':
            return PatientDashboard.objects.all()
        return PatientDashboard.objects.none()

    @action(detail=False, methods=['get'])
    def my_dashboard(self, request):
        """دریافت داشبورد شخصی بیمار"""
        user = request.user
        if user.role != 'Patient':
            return Response(
                {'error': 'دسترسی غیرمجاز'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try:
            dashboard = PatientDashboard.objects.get(patient=user.patientprofile)
        except PatientDashboard.DoesNotExist:
            # ایجاد داشبورد جدید اگر وجود ندارد
            dashboard = PatientDashboard.objects.create(
                patient=user.patientprofile
            )
        
        serializer = self.get_serializer(dashboard)
        return Response(serializer.data)


class AdminDashboardViewSet(viewsets.ViewSet):
    """ویوست برای داشبورد مدیریتی"""
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        """دریافت اطلاعات داشبورد مدیریتی"""
        user = request.user
        if user.role != 'Admin':
            return Response(
                {'error': 'دسترسی غیرمجاز'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # دریافت تنظیمات
        try:
            settings = AdminDashboardSettings.objects.latest('updated_at')
        except AdminDashboardSettings.DoesNotExist:
            settings = AdminDashboardSettings.objects.create()
        
        # آمار کلی
        total_users = User.objects.count()
        total_doctors = DoctorProfile.objects.count()
        total_patients = PatientProfile.objects.count()
        total_appointments = Appointment.objects.count()
        
        # آمار امروز
        today = timezone.now().date()
        today_appointments = Appointment.objects.filter(date=today).count()
        completed_today = Appointment.objects.filter(
            date=today,
            status='completed'
        ).count()
        
        # رشد در هفته اخیر
        week_ago = today - timedelta(days=7)
        new_patients_week = PatientProfile.objects.filter(
            user__date_joined__gte=week_ago
        ).count()
        
        data = {
            'settings': AdminDashboardSettingsSerializer(settings).data,
            'statistics': {
                'total_users': total_users,
                'total_doctors': total_doctors,
                'total_patients': total_patients,
                'total_appointments': total_appointments,
                'today_appointments': today_appointments,
                'completed_today': completed_today,
                'new_patients_week': new_patients_week,
            },
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def charts_data(self, request):
        """دریافت داده‌های نموداری"""
        user = request.user
        if user.role != 'Admin':
            return Response(
                {'error': 'دسترسی غیرمجاز'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # داده‌های نمودار نوبت‌ها در هفته اخیر
        today = timezone.now().date()
        chart_data = []
        for i in range(7):
            date = today - timedelta(days=i)
            count = Appointment.objects.filter(date=date).count()
            chart_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'appointments': count,
            })
        
        return Response({'chart_data': chart_data})


class AdminDashboardSettingsViewSet(viewsets.ModelViewSet):
    """ویوست برای تنظیمات داشبورد مدیریتی"""
    queryset = AdminDashboardSettings.objects.all()
    serializer_class = AdminDashboardSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'Admin':
            return AdminDashboardSettings.objects.all()
        return AdminDashboardSettings.objects.none()
