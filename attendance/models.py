from django.db import models
from django.conf import settings


class Attendance(models.Model):
    """
    Attendance Model
    ----------------
    Ye model student ki daily attendance store karta hai.
    """

    # Attendance status ke choices
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    # Student jiska attendance mark ho raha hai
    # AUTH_USER_MODEL use kiya gaya hai (Custom User model)
    # limit_choices_to ensure karta hai ki sirf STUDENT role wale hi select ho
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        limit_choices_to={'role': 'STUDENT'}
    )

    # Kis date ki attendance hai
    date = models.DateField()

    # Attendance status (Present / Absent)
    # Default Absent rakha gaya hai (safe practice)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    # Teacher jisne attendance mark ki
    # Agar teacher delete ho jaaye to attendance safe rahe (SET_NULL)
    # Sirf TEACHER role wale users allow honge
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance',
        limit_choices_to={'role': 'TEACHER'}
    )

    # Record kab create hua
    created_at = models.DateTimeField(auto_now_add=True)

    # Record kab last update hua
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Same student ke liye same date par duplicate attendance prevent karega
        unique_together = ('student', 'date')

        # Latest date wali attendance pehle dikhegi
        ordering = ['-date']

        # Django admin ke liye readable name
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        # Admin / shell me readable format
        return f"{self.student.username} | {self.date} | {self.get_status_display()}"
