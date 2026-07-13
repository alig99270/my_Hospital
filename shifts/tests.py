from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from accounts.models import User, DoctorProfile
from shifts.models import Shift


class ShiftModelTest(TestCase):
    """Test cases for Shift model"""

    def setUp(self):
        self.doctor_user = User.objects.create_user(
            username='dr_shift_test',
            email='dr_shift@example.com',
            password='testpass123',
            role='Doctor'
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialization='Cardiology',
            department='Internal Medicine'
        )
        self.shift1 = Shift.objects.create(
            doctor=self.doctor_profile,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=4),
            status='available'
        )

    def test_shift_creation(self):
        """Test shift is created correctly"""
        self.assertEqual(self.shift1.doctor, self.doctor_profile)
        self.assertEqual(self.shift1.status, 'available')

    def test_shift_str_method(self):
        """Test shift string representation"""
        expected_str = f"dr_shift_test's Shift ({self.shift1.start_time} - {self.shift1.end_time})"
        self.assertEqual(str(self.shift1), expected_str)

    def test_shift_no_overlapping(self):
        """Test that overlapping shifts are not allowed"""
        with self.assertRaises(ValidationError):
            Shift.objects.create(
                doctor=self.doctor_profile,
                start_time=self.shift1.start_time + timedelta(hours=1),
                end_time=self.shift1.end_time + timedelta(hours=1),
                status='available'
            )

    def test_shift_manager_get_overlapping_shifts(self):
        """Test ShiftManager.get_overlapping_shifts method"""
        # Create a non-overlapping shift
        shift2 = Shift.objects.create(
            doctor=self.doctor_profile,
            start_time=timezone.now() + timedelta(days=2),
            end_time=timezone.now() + timedelta(days=2, hours=4),
            status='available'
        )
        
        # Check for overlaps with the first shift's time range
        has_overlap = Shift.objects.get_overlapping_shifts(
            doctor=self.doctor_profile,
            start_time=self.shift1.start_time,
            end_time=self.shift1.end_time
        )
        self.assertTrue(has_overlap)
        
        # Check for overlaps with a different time range (no overlap)
        has_no_overlap = Shift.objects.get_overlapping_shifts(
            doctor=self.doctor_profile,
            start_time=timezone.now() + timedelta(days=5),
            end_time=timezone.now() + timedelta(days=5, hours=2)
        )
        self.assertFalse(has_no_overlap)

    def test_shift_status_choices(self):
        """Test shift status choices"""
        statuses = ['available', 'booked', 'cancelled']
        for status in statuses:
            shift = Shift.objects.create(
                doctor=self.doctor_profile,
                start_time=timezone.now() + timedelta(days=2),
                end_time=timezone.now() + timedelta(days=2, hours=4),
                status=status
            )
            self.assertEqual(shift.status, status)

    def test_shift_cascade_delete(self):
        """Test shift is deleted when doctor profile is deleted"""
        shift_id = self.shift1.id
        self.doctor_profile.delete()
        self.assertFalse(Shift.objects.filter(id=shift_id).exists())
