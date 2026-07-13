from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from notifications.models import Notification, SMSLog, NotificationTemplate


class NotificationModelTest(TestCase):
    """Test cases for Notification model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='notif_user',
            email='notif@example.com',
            password='testpass123',
            role='Patient'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            title='Test Notification',
            message='This is a test notification',
            notification_type='in_app',
            priority='medium',
            status='pending'
        )

    def test_notification_creation(self):
        """Test notification is created correctly"""
        self.assertEqual(self.notification.title, 'Test Notification')
        self.assertEqual(self.notification.notification_type, 'in_app')
        self.assertEqual(self.notification.priority, 'medium')
        self.assertEqual(self.notification.status, 'pending')

    def test_notification_str_method(self):
        """Test notification string representation"""
        expected_str = "Test Notification - notif_user"
        self.assertEqual(str(self.notification), expected_str)

    def test_notification_without_user(self):
        """Test notification without user (public notification)"""
        public_notif = Notification.objects.create(
            title='Public Announcement',
            message='Important announcement for all users',
            notification_type='in_app',
            priority='high',
            status='pending'
        )
        expected_str = "Public Announcement - عمومی"
        self.assertEqual(str(public_notif), expected_str)

    def test_notification_status_choices(self):
        """Test notification status choices"""
        statuses = ['pending', 'sent', 'failed', 'read']
        for status in statuses:
            notif = Notification.objects.create(
                user=self.user,
                title=f'Test {status}',
                message='Test message',
                status=status
            )
            self.assertEqual(notif.status, status)

    def test_notification_type_choices(self):
        """Test notification type choices"""
        types = ['sms', 'email', 'push', 'in_app']
        for notif_type in types:
            notif = Notification.objects.create(
                user=self.user,
                title=f'Test {notif_type}',
                message='Test message',
                notification_type=notif_type
            )
            self.assertEqual(notif.notification_type, notif_type)

    def test_notification_priority_choices(self):
        """Test notification priority choices"""
        priorities = ['low', 'medium', 'high', 'urgent']
        for priority in priorities:
            notif = Notification.objects.create(
                user=self.user,
                title=f'Test {priority}',
                message='Test message',
                priority=priority
            )
            self.assertEqual(notif.priority, priority)

    def test_notification_recipient_fields(self):
        """Test notification recipient fields"""
        notif = Notification.objects.create(
            user=self.user,
            title='SMS Notification',
            message='Test SMS',
            notification_type='sms',
            recipient_phone='+989123456789',
            recipient_email='test@example.com'
        )
        self.assertEqual(notif.recipient_phone, '+989123456789')
        self.assertEqual(notif.recipient_email, 'test@example.com')


class SMSLogModelTest(TestCase):
    """Test cases for SMSLog model"""

    def setUp(self):
        self.sms_log = SMSLog.objects.create(
            recipient='+989123456789',
            message='Test SMS message',
            status='pending',
            provider='default',
            cost=1000
        )

    def test_sms_log_creation(self):
        """Test SMS log is created correctly"""
        self.assertEqual(self.sms_log.recipient, '+989123456789')
        self.assertEqual(self.sms_log.status, 'pending')
        self.assertEqual(self.sms_log.provider, 'default')
        self.assertEqual(self.sms_log.cost, 1000)

    def test_sms_log_str_method(self):
        """Test SMS log string representation"""
        expected_str = "SMS به +989123456789 - pending"
        self.assertEqual(str(self.sms_log), expected_str)

    def test_sms_log_status_choices(self):
        """Test SMS log status choices"""
        statuses = ['pending', 'sent', 'failed']
        for status in statuses:
            sms = SMSLog.objects.create(
                recipient='+989123456789',
                message=f'Test {status} SMS',
                status=status
            )
            self.assertEqual(sms.status, status)

    def test_sms_log_with_error(self):
        """Test SMS log with error message"""
        sms = SMSLog.objects.create(
            recipient='+989123456789',
            message='Failed SMS',
            status='failed',
            error_message='Provider timeout',
            provider='provider_x'
        )
        self.assertEqual(sms.status, 'failed')
        self.assertEqual(sms.error_message, 'Provider timeout')


class NotificationTemplateModelTest(TestCase):
    """Test cases for NotificationTemplate model"""

    def setUp(self):
        self.template = NotificationTemplate.objects.create(
            name='Appointment Reminder',
            subject='Reminder: Your Appointment Tomorrow',
            body='Dear {{patient_name}}, this is a reminder for your appointment with Dr. {{doctor_name}}.',
            notification_type='sms',
            is_active=True
        )

    def test_template_creation(self):
        """Test notification template is created correctly"""
        self.assertEqual(self.template.name, 'Appointment Reminder')
        self.assertEqual(self.template.notification_type, 'sms')
        self.assertTrue(self.template.is_active)

    def test_template_str_method(self):
        """Test notification template string representation"""
        self.assertEqual(str(self.template), 'Appointment Reminder')

    def test_template_inactive(self):
        """Test inactive template"""
        template = NotificationTemplate.objects.create(
            name='Inactive Template',
            subject='Test',
            body='Test body',
            notification_type='email',
            is_active=False
        )
        self.assertFalse(template.is_active)
