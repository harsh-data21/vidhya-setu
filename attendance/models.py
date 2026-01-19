from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone


class Attendance(models.Model):
    """
    Attendance Model
    ----------------
    Ye model student ki daily attendance store karta hai.

    Rules:
    - Ek student ki ek date par sirf ek attendance hogi
    - Attendance sirf STUDENT ke liye mark hogi
    - Attendance sirf TEACHER ke dwara mark hogi
    """

    # --------------------
    # Attendance Status
    # --------------------
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    # --------------------
    # Student (attendance kiski hai)
    # --------------------
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        limit_choices_to={'role': 'STUDENT'}
    )

    # --------------------
    # Attendance Date
    # --------------------
    date = models.DateField(
        default=timezone.localdate
    )

    # --------------------
    # Attendance Status
    # --------------------
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    # --------------------
    # Teacher who marked attendance
    # --------------------
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance',
        limit_choices_to={'role': 'TEACHER'}
    )

    # --------------------
    # Timestamps
    # --------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --------------------
    # Model-level validation
    # --------------------
    def clean(self):
        # Student validation
        if self.student and getattr(self.student, 'role', None) != 'STUDENT':
            raise ValidationError("Attendance sirf STUDENT ke liye mark ho sakti hai.")

        # Teacher validation
        if self.marked_by and getattr(self.marked_by, 'role', None) != 'TEACHER':
            raise ValidationError("Attendance sirf TEACHER ke dwara mark ho sakti hai.")

    # --------------------
    # Ensure clean() runs
    # --------------------
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # --------------------
    # Meta Configuration
    # --------------------
    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date', 'student']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['student', 'date']),
        ]

    # --------------------
    # String Representation
    # --------------------
    def __str__(self):
        return f"{self.student.username} | {self.date} | {self.get_status_display()}"
