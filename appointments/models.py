from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import DoctorProfile, PatientProfile
from shifts.models import Shift


APPOINTMENT_STATUS_CHOICES = [
    ('booked', 'Booked'),
    ('canceled', 'Canceled'),
    ('completed', 'Completed'),
]


class AppointmentManager(models.Manager):
    """Custom manager for Appointment model to handle overlap checks."""

    def get_overlapping_appointments(self, doctor, patient, start_time, end_time, exclude_id=None):
        """Find appointments that overlap with the given time range."""
        queryset_doctor = self.filter(
            doctor=doctor,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        queryset_patient = self.filter(
            patient=patient,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if exclude_id is not None:
            queryset_doctor = queryset_doctor.exclude(id=exclude_id)
            queryset_patient = queryset_patient.exclude(id=exclude_id)
        
        return queryset_doctor.exists() or queryset_patient.exists()


class Appointment(models.Model):
    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    shift = models.ForeignKey(
        Shift,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=APPOINTMENT_STATUS_CHOICES,
        default='booked'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = AppointmentManager()

    class Meta:
        ordering = ['start_time']

    def clean(self):
        self._validate_shift_times()
        self._validate_no_overlaps()

    def _validate_shift_times(self):
        """Ensure appointment is within shift times."""
        if self.shift:
            if not (self.shift.start_time <= self.start_time and self.end_time <= self.shift.end_time):
                raise ValidationError("Appointment must be within shift times")

    def _validate_no_overlaps(self):
        """Prevent overlapping appointments for the same doctor or patient."""
        if Appointment.objects.get_overlapping_appointments(
            doctor=self.doctor,
            patient=self.patient,
            start_time=self.start_time,
            end_time=self.end_time,
            exclude_id=self.id
        ):
            raise ValidationError("Appointment cannot overlap with existing appointments")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.username} for {self.patient.full_name}"