from django.db import models
from accounts.models import DoctorProfile, PatientProfile
from shifts.models import Shift
from django.core.exceptions import ValidationError

APPOINTMENT_STATUS_CHOICES = [
    ('booked', 'Booked'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
]

class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='appointments')
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def clean(self):
        # Ensure appointment is within shift times
        if self.shift and not (self.shift.start_time <= self.start_time and self.end_time <= self.shift.end_time):
            raise ValidationError("Appointment must be within shift times")

        # Prevent overlapping appointments for the same doctor or patient [[2]]
        overlapping_doctor = Appointment.objects.filter(
            doctor=self.doctor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        overlapping_patient = Appointment.objects.filter(
            patient=self.patient,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping_doctor.exists() or overlapping_patient.exists():
            raise ValidationError("Appointment cannot overlap with existing appointments")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.username} for {self.patient.full_name}"