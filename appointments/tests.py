from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from django.core.exceptions import ValidationError
from accounts.models import User, PatientProfile, DoctorProfile
from shifts.models import Shift
from appointments.models import Appointment
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class AppointmentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.appointment_url = reverse('appointment-list')

        # Create Doctor
        self.doctor_user = User.objects.create_user(
            username="doctor_john",
            email="doctor@example.com",
            password="A@123456789",
            role="Doctor"
        )
        DoctorProfile.objects.create(user=self.doctor_user, specialization="Cardiology", department="Internal Medicine")

        # Create Shift with timezone-aware times
        self.shift = Shift.objects.create(
            doctor=self.doctor_user.doctorprofile,
            start_time=timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 0)),
            end_time=timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 30)),
            status="available"
        )

        # Create Patient
        self.patient_user = User.objects.create_user(
            username="patient_jane",
            email="patient@example.com",
            password="A@123456789",
            role="Patient"
        )
        PatientProfile.objects.create(
            user=self.patient_user,
            full_name="Jane Doe",
            date_of_birth="1990-01-01",
            gender="Female",
            email="patient@example.com",
            phone="1234567890"
        )

        # Generate JWT Token for Patient
        refresh = RefreshToken.for_user(self.patient_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_appointment_success(self):
        """Test successful appointment creation via API"""
        payload = {
            "patient_id": self.patient_user.id,
            "doctor_id": self.doctor_user.id,
            "shift_id": self.shift.id,
            "start_time": timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 0)),
            "end_time": timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 30)),
            "status": "booked"
        }

        response = self.client.post(self.appointment_url, data=payload)
        print(response.content)

        self.assertEqual(response.status_code, 201)
        appointment = Appointment.objects.get(id=response.data["id"])
        self.assertEqual(appointment.status, "booked")
        self.assertEqual(appointment.doctor.user.id, self.doctor_user.id)
        self.assertEqual(appointment.patient.user.id, self.patient_user.id)


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


class AppointmentModelTest(TestCase):
    """Test cases for Appointment model"""

    def setUp(self):
        # Create doctor
        self.doctor_user = User.objects.create_user(
            username='dr_appt_test',
            email='dr_appt@example.com',
            password='testpass123',
            role='Doctor'
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialization='Cardiology',
            department='Internal Medicine'
        )
        
        # Create patient
        self.patient_user = User.objects.create_user(
            username='patient_appt_test',
            email='patient_appt@example.com',
            password='testpass123',
            role='Patient'
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.patient_user,
            full_name='Test Patient',
            date_of_birth='1990-01-01',
            gender='Male',
            email='patient_appt@test.com',
            phone='1234567890'
        )
        
        # Create shift
        self.shift = Shift.objects.create(
            doctor=self.doctor_profile,
            start_time=timezone.now() + timedelta(days=1),
            end_time=timezone.now() + timedelta(days=1, hours=8),
            status='available'
        )
        
        # Create appointment
        self.appointment = Appointment.objects.create(
            patient=self.patient_profile,
            doctor=self.doctor_profile,
            shift=self.shift,
            start_time=timezone.now() + timedelta(days=1, hours=1),
            end_time=timezone.now() + timedelta(days=1, hours=2),
            status='booked'
        )

    def test_appointment_creation(self):
        """Test appointment is created correctly"""
        self.assertEqual(self.appointment.patient, self.patient_profile)
        self.assertEqual(self.appointment.doctor, self.doctor_profile)
        self.assertEqual(self.appointment.status, 'booked')

    def test_appointment_str_method(self):
        """Test appointment string representation"""
        expected_str = f"Appointment with Dr. dr_appt_test for Test Patient"
        self.assertEqual(str(self.appointment), expected_str)

    def test_appointment_within_shift_times(self):
        """Test appointment must be within shift times"""
        self.assertIsNotNone(self.appointment)
        
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient_profile,
                doctor=self.doctor_profile,
                shift=self.shift,
                start_time=self.shift.start_time - timedelta(hours=2),
                end_time=self.shift.start_time - timedelta(hours=1),
                status='booked'
            )

    def test_appointment_no_overlapping_for_doctor(self):
        """Test that overlapping appointments for the same doctor are not allowed"""
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient_profile,
                doctor=self.doctor_profile,
                shift=self.shift,
                start_time=self.appointment.start_time + timedelta(minutes=30),
                end_time=self.appointment.end_time + timedelta(minutes=30),
                status='booked'
            )

    def test_appointment_no_overlapping_for_patient(self):
        """Test that overlapping appointments for the same patient are not allowed"""
        doctor2_user = User.objects.create_user(
            username='dr_appt_test2',
            email='dr_appt2@example.com',
            password='testpass123',
            role='Doctor'
        )
        doctor2_profile = DoctorProfile.objects.create(
            user=doctor2_user,
            specialization='Neurology',
            department='Neurology'
        )
        
        with self.assertRaises(ValidationError):
            Appointment.objects.create(
                patient=self.patient_profile,
                doctor=doctor2_profile,
                start_time=self.appointment.start_time + timedelta(minutes=30),
                end_time=self.appointment.end_time + timedelta(minutes=30),
                status='booked'
            )

    def test_appointment_manager_get_overlapping_appointments(self):
        """Test AppointmentManager.get_overlapping_appointments method"""
        has_overlap = Appointment.objects.get_overlapping_appointments(
            doctor=self.doctor_profile,
            patient=self.patient_profile,
            start_time=self.appointment.start_time,
            end_time=self.appointment.end_time
        )
        self.assertTrue(has_overlap)
        
        has_no_overlap_excluding = Appointment.objects.get_overlapping_appointments(
            doctor=self.doctor_profile,
            patient=self.patient_profile,
            start_time=self.appointment.start_time,
            end_time=self.appointment.end_time,
            exclude_id=self.appointment.id
        )
        self.assertFalse(has_no_overlap_excluding)

    def test_appointment_status_choices(self):
        """Test appointment status choices"""
        statuses = ['booked', 'canceled', 'completed']
        for status in statuses:
            appt = Appointment.objects.create(
                patient=self.patient_profile,
                doctor=self.doctor_profile,
                shift=self.shift,
                start_time=timezone.now() + timedelta(days=2),
                end_time=timezone.now() + timedelta(days=2, hours=1),
                status=status
            )
            self.assertEqual(appt.status, status)