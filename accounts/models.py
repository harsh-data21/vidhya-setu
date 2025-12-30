from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ==================================================
# CUSTOM USER MODEL
# ==================================================
class User(AbstractUser):
    """
    Custom User model
    - AbstractUser se inherit kiya gaya hai
    - role field add ki gayi hai (Admin / Teacher / Student)
    """

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT',   # by default student
        db_index=True        # role-based queries fast hongi
    )

    def __str__(self):
        # Admin panel aur debugging ke liye readable output
        return self.username


# ==================================================
# TEACHER PROFILE
# ==================================================
class TeacherProfile(models.Model):
    """
    Teacher ka extra data store karne ke liye
    User table clean rehti hai
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    subject = models.CharField(
        max_length=100,
        help_text="Subject taught by the teacher"
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Teacher: {self.user.username}"


# ==================================================
# STUDENT PROFILE
# ==================================================
class StudentProfile(models.Model):
    """
    Student ka extra data
    Roll number, phone etc.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    roll_no = models.CharField(
        max_length=20,
        unique=True,     # ek hi roll number repeat na ho
        db_index=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"Student: {self.user.username}"


# ==================================================
# HOMEWORK MODEL
# ==================================================
class Homework(models.Model):
    """
    Homework module
    - Teacher homework add karega
    - Student sirf view karega
    """

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='homeworks',
        limit_choices_to={'role': 'TEACHER'}
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()

    due_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['due_date']   # nearest due date pehle
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return f"{self.title} (Due: {self.due_date})"
