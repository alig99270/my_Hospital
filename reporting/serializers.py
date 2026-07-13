from rest_framework import serializers
from .models import Report, AppointmentStatistics, PatientStatistics, FinancialReport


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ['created_at', 'generated_by']


class AppointmentStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppointmentStatistics
        fields = '__all__'


class PatientStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientStatistics
        fields = '__all__'


class FinancialReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialReport
        fields = '__all__'
