from django.test import TestCase
from django.utils import timezone
from accounts.models import User, PatientProfile
from dashboard.models import DashboardWidget, DashboardMetric, PatientDashboard, AdminDashboardSettings


class DashboardWidgetModelTest(TestCase):
    """Test cases for DashboardWidget model"""

    def setUp(self):
        self.widget = DashboardWidget.objects.create(
            name='Appointments Chart',
            widget_type='chart',
            description='Shows appointments over time',
            configuration={'type': 'line', 'data_source': 'appointments'},
            is_active=True,
            order=1
        )

    def test_widget_creation(self):
        """Test dashboard widget is created correctly"""
        self.assertEqual(self.widget.name, 'Appointments Chart')
        self.assertEqual(self.widget.widget_type, 'chart')
        self.assertTrue(self.widget.is_active)
        self.assertEqual(self.widget.order, 1)

    def test_widget_str_method(self):
        """Test dashboard widget string representation"""
        self.assertEqual(str(self.widget), 'Appointments Chart')

    def test_widget_type_choices(self):
        """Test widget type choices"""
        types = ['statistics', 'chart', 'table', 'calendar', 'alerts']
        for widget_type in types:
            widget = DashboardWidget.objects.create(
                name=f'Test {widget_type} Widget',
                widget_type=widget_type,
                is_active=True
            )
            self.assertEqual(widget.widget_type, widget_type)


class DashboardMetricModelTest(TestCase):
    """Test cases for DashboardMetric model"""

    def setUp(self):
        self.metric = DashboardMetric.objects.create(
            name='Total Appointments Today',
            metric_type='appointments',
            value=50,
            change_percentage=10.5,
            date=timezone.now().date()
        )

    def test_metric_creation(self):
        """Test dashboard metric is created correctly"""
        self.assertEqual(self.metric.name, 'Total Appointments Today')
        self.assertEqual(self.metric.metric_type, 'appointments')
        self.assertEqual(self.metric.value, 50)
        self.assertEqual(self.metric.change_percentage, 10.5)

    def test_metric_str_method(self):
        """Test dashboard metric string representation"""
        expected_str = f"Total Appointments Today - {self.metric.date}"
        self.assertEqual(str(self.metric), expected_str)

    def test_metric_type_choices(self):
        """Test metric type choices"""
        types = ['appointments', 'patients', 'doctors', 'revenue', 'prescriptions']
        for metric_type in types:
            metric = DashboardMetric.objects.create(
                name=f'Test {metric_type} Metric',
                metric_type=metric_type,
                value=100,
                date=timezone.now().date()
            )
            self.assertEqual(metric.metric_type, metric_type)


class PatientDashboardModelTest(TestCase):
    """Test cases for PatientDashboard model"""

    def setUp(self):
        self.patient_user = User.objects.create_user(
            username='patient_dash_test',
            email='patient_dash@example.com',
            password='testpass123',
            role='Patient'
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient_user,
            full_name='Test Patient Dashboard',
            date_of_birth='1990-01-01',
            gender='Male',
            email='patient_dash@test.com',
            phone='1234567890'
        )
        self.dashboard = PatientDashboard.objects.create(
            patient=self.patient_profile,
            pending_prescriptions=2,
            unread_notifications=5,
            health_score=85
        )

    def test_patient_dashboard_creation(self):
        """Test patient dashboard is created correctly"""
        self.assertEqual(self.dashboard.patient, self.patient_profile)
        self.assertEqual(self.dashboard.pending_prescriptions, 2)
        self.assertEqual(self.dashboard.unread_notifications, 5)
        self.assertEqual(self.dashboard.health_score, 85)

    def test_patient_dashboard_str_method(self):
        """Test patient dashboard string representation"""
        expected_str = "داشبورد Test Patient Dashboard"
        self.assertEqual(str(self.dashboard), expected_str)

    def test_patient_dashboard_default_values(self):
        """Test patient dashboard default values"""
        # Create a new patient profile for this test to avoid unique constraint
        patient_user2 = User.objects.create_user(
            username='patient_dash_test2',
            email='patient_dash2@example.com',
            password='testpass123',
            role='Patient'
        )
        patient_profile2 = PatientProfile.objects.create(
            user=patient_user2,
            full_name='Test Patient Dashboard 2',
            date_of_birth='1990-01-02',
            gender='Female',
            email='patient_dash2@test.com',
            phone='1234567891'
        )
        dashboard = PatientDashboard.objects.create(
            patient=patient_profile2
        )
        self.assertEqual(dashboard.pending_prescriptions, 0)
        self.assertEqual(dashboard.unread_notifications, 0)
        self.assertEqual(dashboard.health_score, 0)
        self.assertIsNone(dashboard.last_visit)
        self.assertIsNone(dashboard.next_appointment)


class AdminDashboardSettingsModelTest(TestCase):
    """Test cases for AdminDashboardSettings model"""

    def setUp(self):
        self.settings = AdminDashboardSettings.objects.create(
            refresh_interval=300,
            show_real_time_stats=True,
            default_date_range=30,
            max_records_per_page=20,
            enable_export=True
        )

    def test_settings_creation(self):
        """Test admin dashboard settings is created correctly"""
        self.assertEqual(self.settings.refresh_interval, 300)
        self.assertTrue(self.settings.show_real_time_stats)
        self.assertEqual(self.settings.default_date_range, 30)
        self.assertEqual(self.settings.max_records_per_page, 20)
        self.assertTrue(self.settings.enable_export)

    def test_settings_str_method(self):
        """Test admin dashboard settings string representation"""
        self.assertEqual(str(self.settings), "تنظیمات داشبورد مدیریتی")

    def test_settings_default_values(self):
        """Test admin dashboard settings default values"""
        settings = AdminDashboardSettings.objects.create()
        self.assertEqual(settings.refresh_interval, 300)
        self.assertTrue(settings.show_real_time_stats)
        self.assertEqual(settings.default_date_range, 30)
        self.assertEqual(settings.max_records_per_page, 20)
        self.assertTrue(settings.enable_export)
