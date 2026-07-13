from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSet,
    AppointmentStatisticsViewSet,
    PatientStatisticsViewSet,
    FinancialReportViewSet,
)

router = DefaultRouter()
router.register(r'reports', ReportViewSet)
router.register(r'appointment-stats', AppointmentStatisticsViewSet)
router.register(r'patient-stats', PatientStatisticsViewSet)
router.register(r'financial-reports', FinancialReportViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
