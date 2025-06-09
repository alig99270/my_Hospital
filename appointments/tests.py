from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from accounts.models import User, PatientProfile, DoctorProfile
from shifts.models import Shift
from appointments.models import Appointment
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

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
        # Arrange
        payload = {
            "patient_id": self.patient_user.id,  # ✅ Use User.id
            "doctor_id": self.doctor_user.id,     # ✅ Use User.id
            "shift_id": self.shift.id,
            "start_time": timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 0)),
            "end_time": timezone.make_aware(timezone.datetime(2025, 5, 20, 10, 30)),
            "status": "booked"
        }

        # Act
        response = self.client.post(self.appointment_url, data=payload)
        print(response.content)  # 🔍 View detailed error

        # Assert
        self.assertEqual(response.status_code, 201)
        appointment = Appointment.objects.get(id=response.data["id"])
        self.assertEqual(appointment.status, "booked")
        self.assertEqual(appointment.doctor.user.id, self.doctor_user.id)
        self.assertEqual(appointment.patient.user.id, self.patient_user.id)