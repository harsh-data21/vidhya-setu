from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone


# ==================================================
# CUSTOM USER MODEL
# ==================================================
class User(AbstractUser):
    """
    Custom User Model
    -----------------
    Role-based authentication system
    """

    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='STUDENT',
        db_index=True
    )

    def __str__(self):
        return self.username


# ==================================================
# TEACHER PROFILE
# ==================================================
class TeacherProfile(models.Model):
    """
    Teacher Profile
    Admin assigns class & section here
    """

    DESIGNATION_CHOICES = (
        ('PRINCIPAL', 'Principal'),
        ('SENIOR', 'Senior Teacher'),
        ('ASSISTANT', 'Assistant Teacher'),
    )

    CLASS_CHOICES = (
        ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'),
        ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'),
        ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'),
        ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'),
    )

    SECTION_CHOICES = (
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    designation = models.CharField(
        max_length=20,
        choices=DESIGNATION_CHOICES,
        default='ASSISTANT'
    )

    # 🔥 Subject specialization (text is fine)
    subject = models.CharField(
        max_length=100,
        help_text="Main subject handled by teacher"
    )

    # 🔥 Admin assigns these
    assigned_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES,
        null=True,
        blank=True
    )

    assigned_section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} | {self.subject} | {self.assigned_class}{self.assigned_section}"


# ==================================================
# STUDENT PROFILE
# ==================================================
class StudentProfile(models.Model):
    """
    Student Profile
    """

    CLASS_CHOICES = (
        ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'),
        ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'),
        ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'),
        ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'),
    )

    SECTION_CHOICES = (
        ('A', 'Section A'),
        ('B', 'Section B'),
        ('C', 'Section C'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    student_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES,
        null=True,
        blank=True
    )

    section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES,
        null=True,
        blank=True
    )

    roll_no = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    dob = models.DateField(
        null=True,
        blank=True
    )

    father_name = models.CharField(
        max_length=100,
        blank=True
    )

    contact_number = models.CharField(
        max_length=15,
        blank=True
    )

    class Meta:
        ordering = ['student_class', 'section', 'roll_no']
        unique_together = ('student_class', 'section', 'roll_no')

    def __str__(self):
        return f"{self.user.username} | Class {self.student_class}{self.section} | Roll {self.roll_no}"


# ==================================================
# HOMEWORK MODEL
# ==================================================
class Homework(models.Model):
    """
    Homework Model
    """

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='homeworks',
        limit_choices_to={'role': 'TEACHER'}
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['due_date']
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return f"{self.title} | Due: {self.due_date}"


# ==================================================
# NOTICE MODEL
# ==================================================
class Notice(models.Model):
    """
    Notice Model
    ------------

    Admin / Teacher create
    Student / Teacher view
    """

    title = models.CharField(max_length=200)
    message = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='notices'
    )

    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'

    def __str__(self):
        return self.title
