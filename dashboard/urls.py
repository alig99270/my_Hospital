from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    DashboardWidgetViewSet,
    DashboardMetricViewSet,
    PatientDashboardViewSet,
    AdminDashboardViewSet,
    AdminDashboardSettingsViewSet,
)

router = DefaultRouter()
router.register(r'widgets', DashboardWidgetViewSet)
router.register(r'metrics', DashboardMetricViewSet)
router.register(r'patient-dashboard', PatientDashboardViewSet)
router.register(r'settings', AdminDashboardSettingsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin-dashboard/', AdminDashboardViewSet.as_view({'get': 'list'}), name='admin-dashboard'),
    path('admin-dashboard/charts-data/', AdminDashboardViewSet.as_view({'get': 'charts_data'}), name='admin-dashboard-charts'),
]
