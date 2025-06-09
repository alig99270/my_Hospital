from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Staff', 'Staff'),
        ('Patient', 'Patient'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Patient')

    def __str__(self):
        return f"{self.username} ({self.role})"


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialization = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"


class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.position}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    profile_photo = models.BinaryField(null=True, blank=True)
    medical_history_summary = models.TextField(blank=True)

    def __str__(self):
        return self.full_name