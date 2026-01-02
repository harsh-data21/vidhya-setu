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
    # Default = today (BEST PRACTICE)
    # --------------------
    date = models.DateField(
        default=timezone.now
    )

    # --------------------
    # Attendance Status
    # Default = Absent (safe practice)
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
    # Model-level validation (extra safety)
    # --------------------
    def clean(self):
        """
        Extra validation:
        - Student role must be STUDENT
        - Marked_by role must be TEACHER
        """
        if self.student and self.student.role != 'STUDENT':
            raise ValidationError("Attendance can only be marked for students.")

        if self.marked_by and self.marked_by.role != 'TEACHER':
            raise ValidationError("Attendance can only be marked by a teacher.")

    # --------------------
    # Meta Configuration
    # --------------------
    class Meta:
        # Same student + same date = no duplicate attendance
        unique_together = ('student', 'date')

        # Latest attendance first
        ordering = ['-date', 'student']

        # Admin display names
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'

        # Database optimization
        indexes = [
            models.Index(fields=['student', 'date']),
        ]

    # --------------------
    # String Representation
    # --------------------
    def __str__(self):
        return f"{self.student.username} | {self.date} | {self.get_status_display()}"
