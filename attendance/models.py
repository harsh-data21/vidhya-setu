from django.db import models
from django.conf import settings


class Attendance(models.Model):

    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attendance_records',
        limit_choices_to={'role': 'STUDENT'}
    )

    date = models.DateField()

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='A'
    )

    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='marked_attendance',
        limit_choices_to={'role': 'TEACHER'}
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'date')   # ek din me ek attendance
        ordering = ['-date']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.student.username} | {self.date} | {self.get_status_display()}"
