from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import DoctorProfile


SHIFT_STATUS_CHOICES = [
    ('available', 'Available'),
    ('booked', 'Booked'),
    ('cancelled', 'Cancelled'),
]


class ShiftManager(models.Manager):
    """Custom manager for Shift model to handle overlap checks."""

    def get_overlapping_shifts(self, doctor, start_time, end_time, exclude_id=None):
        """Find shifts that overlap with the given time range."""
        queryset = self.filter(
            doctor=doctor,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        
        if exclude_id is not None:
            queryset = queryset.exclude(id=exclude_id)
        
        return queryset.exists()


class Shift(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='shifts'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=10,
        choices=SHIFT_STATUS_CHOICES,
        default='available'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ShiftManager()

    class Meta:
        ordering = ['start_time']

    def clean(self):
        self._validate_no_overlaps()

    def _validate_no_overlaps(self):
        """Prevent overlapping shifts for the same doctor."""
        if Shift.objects.get_overlapping_shifts(
            doctor=self.doctor,
            start_time=self.start_time,
            end_time=self.end_time,
            exclude_id=self.id
        ):
            raise ValidationError("Shift cannot overlap with existing shifts")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doctor.user.username}'s Shift ({self.start_time} - {self.end_time})"