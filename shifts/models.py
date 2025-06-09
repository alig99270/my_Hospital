from django.db import models
from accounts.models import DoctorProfile
from django.core.exceptions import ValidationError

class Shift(models.Model):
    SHIFT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='shifts')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=SHIFT_STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def clean(self):
        # Prevent overlapping shifts for the same doctor [[3]]
        overlapping_shifts = Shift.objects.filter(
            doctor=self.doctor,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        if overlapping_shifts.exists():
            raise ValidationError("Shift cannot overlap with existing shifts")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.user.username}'s Shift ({self.start_time} - {self.end_time})"