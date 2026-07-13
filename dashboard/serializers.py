from rest_framework import serializers
from .models import DashboardWidget, DashboardMetric, PatientDashboard, AdminDashboardSettings


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = '__all__'


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = '__all__'


class PatientDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDashboard
        fields = '__all__'
        read_only_fields = ['patient']


class AdminDashboardSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminDashboardSettings
        fields = '__all__'
        read_only_fields = ['updated_at']
