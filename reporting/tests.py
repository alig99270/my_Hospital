from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, DoctorProfile, PatientProfile
from reporting.models import Report, AppointmentStatistics, PatientStatistics, FinancialReport


class ReportModelTest(TestCase):
    """Test cases for Report model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='report_user',
            email='report@example.com',
            password='testpass123',
            role='Admin'
        )
        self.report = Report.objects.create(
            title='Monthly Appointments Report',
            report_type='monthly',
            description='Report of all appointments for the month',
            generated_by=self.user,
            status='pending'
        )

    def test_report_creation(self):
        """Test report is created correctly"""
        self.assertEqual(self.report.title, 'Monthly Appointments Report')
        self.assertEqual(self.report.report_type, 'monthly')
        self.assertEqual(self.report.generated_by, self.user)
        self.assertEqual(self.report.status, 'pending')

    def test_report_str_method(self):
        """Test report string representation"""
        expected_start = "Monthly Appointments Report"
        self.assertIn(expected_start, str(self.report))

    def test_report_status_choices(self):
        """Test report status choices"""
        statuses = ['pending', 'completed', 'failed']
        for status in statuses:
            report = Report.objects.create(
                title=f'Test {status} Report',
                report_type='daily',
                generated_by=self.user,
                status=status
            )
            self.assertEqual(report.status, status)

    def test_report_type_choices(self):
        """Test report type choices"""
        types = ['daily', 'weekly', 'monthly', 'yearly', 'custom']
        for report_type in types:
            report = Report.objects.create(
                title=f'Test {report_type} Report',
                report_type=report_type,
                generated_by=self.user
            )
            self.assertEqual(report.report_type, report_type)


class AppointmentStatisticsModelTest(TestCase):
    """Test cases for AppointmentStatistics model"""

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='dr_stats_test',
            email='dr_stats@example.com',
            password='testpass123',
            role='Doctor'
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialization='Cardiology',
            department='Internal Medicine'
        )
        self.stats = AppointmentStatistics.objects.create(
            date=timezone.now().date(),
            total_appointments=50,
            completed_appointments=40,
            cancelled_appointments=5,
            no_show_appointments=5,
            doctor=self.doctor_profile
        )

    def test_appointment_stats_creation(self):
        """Test appointment statistics is created correctly"""
        self.assertEqual(self.stats.total_appointments, 50)
        self.assertEqual(self.stats.completed_appointments, 40)
        self.assertEqual(self.stats.cancelled_appointments, 5)
        self.assertEqual(self.stats.no_show_appointments, 5)

    def test_appointment_stats_str_method(self):
        """Test appointment statistics string representation"""
        expected_str = f"آمار {self.stats.date} - کل: 50"
        self.assertEqual(str(self.stats), expected_str)

    def test_appointment_stats_without_doctor(self):
        """Test appointment statistics without specific doctor (system-wide)"""
        stats = AppointmentStatistics.objects.create(
            date=timezone.now().date(),
            total_appointments=100,
            completed_appointments=80,
            cancelled_appointments=10,
            no_show_appointments=10
        )
        self.assertIsNone(stats.doctor)


class PatientStatisticsModelTest(TestCase):
    """Test cases for PatientStatistics model"""

    def setUp(self):
        self.stats = PatientStatistics.objects.create(
            date=timezone.now().date(),
            total_patients=500,
            new_patients=25,
            active_patients=450
        )

    def test_patient_stats_creation(self):
        """Test patient statistics is created correctly"""
        self.assertEqual(self.stats.total_patients, 500)
        self.assertEqual(self.stats.new_patients, 25)
        self.assertEqual(self.stats.active_patients, 450)

    def test_patient_stats_str_method(self):
        """Test patient statistics string representation"""
        expected_str = f"آمار بیماران {self.stats.date}"
        self.assertEqual(str(self.stats), expected_str)


class FinancialReportModelTest(TestCase):
    """Test cases for FinancialReport model"""

    def setUp(self):
        self.report = FinancialReport.objects.create(
            date=timezone.now().date(),
            total_revenue=10000000,
            total_expenses=6000000,
            net_profit=4000000,
            description='Monthly financial report'
        )

    def test_financial_report_creation(self):
        """Test financial report is created correctly"""
        self.assertEqual(self.report.total_revenue, 10000000)
        self.assertEqual(self.report.total_expenses, 6000000)
        self.assertEqual(self.report.net_profit, 4000000)

    def test_financial_report_str_method(self):
        """Test financial report string representation"""
        expected_str = f"گزارش مالی {self.report.date}"
        self.assertEqual(str(self.report), expected_str)

    def test_financial_report_calculation(self):
        """Test that net_profit equals revenue minus expenses"""
        report = FinancialReport.objects.create(
            date=timezone.now().date(),
            total_revenue=5000000,
            total_expenses=3000000,
            net_profit=2000000
        )
        self.assertEqual(report.net_profit, report.total_revenue - report.total_expenses)
