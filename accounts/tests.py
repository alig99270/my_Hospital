from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from accounts.models import User, DoctorProfile, StaffProfile, PatientProfile
from accounts.serializers import RegisterSerializer
import json

User = get_user_model()


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_register_doctor_success(self):
        """Test successful doctor registration"""
        payload = {
            "username": "dr_john",
            "email": "john@example.com",
            "password": "A@123456789",
            "role": "Doctor",
            "profile_data": {
                "specialization": "Cardiology",
                "department": "Internal Medicine"
            }
        }

        response = self.client.post(self.register_url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="dr_john")
        self.assertEqual(user.role, "Doctor")
        self.assertTrue(DoctorProfile.objects.filter(user=user).exists())

    def test_register_patient_success(self):
        """Test successful patient registration"""
        payload = {
            "username": "patient1",
            "email": "patient@example.com",
            "password": "P@123456789",
            "role": "Patient",
            "profile_data": {
                "full_name": "John Patient",
                "date_of_birth": "1990-01-01",
                "gender": "Male",
                "phone": "1234567890"
            }
        }

        response = self.client.post(self.register_url, data=json.dumps(payload), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="patient1")
        self.assertEqual(user.role, "Patient")
        self.assertTrue(PatientProfile.objects.filter(user=user).exists())


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='Patient'
        )

    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.role, 'Patient')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str_method(self):
        """Test user string representation"""
        expected_str = "testuser (Patient)"
        self.assertEqual(str(self.user), expected_str)

    def test_user_role_choices(self):
        """Test user role choices"""
        roles = ['Admin', 'Doctor', 'Staff', 'Patient']
        for role in roles:
            user = User.objects.create_user(
                username=f'user_{role.lower()}',
                email=f'{role.lower()}@example.com',
                password='testpass123',
                role=role
            )
            self.assertEqual(user.role, role)


class DoctorProfileModelTest(TestCase):
    """Test cases for DoctorProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='dr_test',
            email='dr@example.com',
            password='testpass123',
            role='Doctor'
        )
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.user,
            specialization='Cardiology',
            department='Internal Medicine'
        )

    def test_doctor_profile_creation(self):
        """Test doctor profile is created correctly"""
        self.assertEqual(self.doctor_profile.specialization, 'Cardiology')
        self.assertEqual(self.doctor_profile.department, 'Internal Medicine')

    def test_doctor_profile_str_method(self):
        """Test doctor profile string representation"""
        expected_str = "Dr. dr_test - Cardiology"
        self.assertEqual(str(self.doctor_profile), expected_str)

    def test_doctor_profile_cascade_delete(self):
        """Test doctor profile is deleted when user is deleted"""
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(DoctorProfile.objects.filter(user_id=user_id).exists())


class StaffProfileModelTest(TestCase):
    """Test cases for StaffProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='staff_test',
            email='staff@example.com',
            password='testpass123',
            role='Staff'
        )
        self.staff_profile = StaffProfile.objects.create(
            user=self.user,
            position='Receptionist'
        )

    def test_staff_profile_creation(self):
        """Test staff profile is created correctly"""
        self.assertEqual(self.staff_profile.position, 'Receptionist')

    def test_staff_profile_str_method(self):
        """Test staff profile string representation"""
        expected_str = "staff_test - Receptionist"
        self.assertEqual(str(self.staff_profile), expected_str)


class PatientProfileModelTest(TestCase):
    """Test cases for PatientProfile model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='patient_test',
            email='patient@example.com',
            password='testpass123',
            role='Patient'
        )
        self.patient_profile = PatientProfile.objects.create(
            user=self.user,
            full_name='Test Patient',
            date_of_birth='1990-01-01',
            gender='Male',
            email='patient@test.com',
            phone='1234567890'
        )

    def test_patient_profile_creation(self):
        """Test patient profile is created correctly"""
        self.assertEqual(self.patient_profile.full_name, 'Test Patient')
        self.assertEqual(self.patient_profile.gender, 'Male')
        self.assertEqual(self.patient_profile.phone, '1234567890')

    def test_patient_profile_str_method(self):
        """Test patient profile string representation"""
        self.assertEqual(str(self.patient_profile), 'Test Patient')

    def test_patient_profile_gender_choices(self):
        """Test patient profile gender choices"""
        genders = ['Male', 'Female', 'Other']
        for gender in genders:
            user = User.objects.create_user(
                username=f'patient_{gender.lower()}',
                email=f'{gender.lower()}@test.com',
                password='testpass123',
                role='Patient'
            )
            profile = PatientProfile.objects.create(
                user=user,
                full_name=f'{gender} Patient',
                date_of_birth='1990-01-01',
                gender=gender,
                email=f'{gender}@test.com',
                phone='1234567890'
            )
            self.assertEqual(profile.gender, gender)