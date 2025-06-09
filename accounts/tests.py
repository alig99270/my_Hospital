from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import User, DoctorProfile
from accounts.serializers import RegisterSerializer
import json

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class RegistrationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')  # Defined in accounts/urls.py

    def test_register_doctor_success(self):
        # Arrange
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

        # Act
        response = self.client.post(self.register_url, data=json.dumps(payload), content_type='application/json')

        # Assert
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="dr_john")
        self.assertEqual(user.role, "Doctor")
        self.assertTrue(DoctorProfile.objects.filter(user=user).exists())