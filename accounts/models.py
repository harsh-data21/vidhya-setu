from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# ==================================================
# CUSTOM USER MODEL
# ==================================================
class User(AbstractUser):
    """
    Custom User Model
    -----------------
    - AbstractUser se inherit
    - Role-based authentication system
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
    ---------------
    - One teacher = one user
    - Class & section assignment
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

    subject = models.CharField(
        max_length=100
    )

    assigned_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES
    )

    assigned_section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES
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
    ---------------
    - Roll number auto-generated from view
    - Class + section wise unique roll no
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

    father_name = models.CharField(
        max_length=100
    )

    contact_number = models.CharField(
        max_length=15
    )

    student_class = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES
    )

    section = models.CharField(
        max_length=1,
        choices=SECTION_CHOICES
    )

    roll_no = models.PositiveIntegerField()

    class Meta:
        unique_together = ('student_class', 'section', 'roll_no')
        ordering = ['student_class', 'section', 'roll_no']

    def __str__(self):
        return f"{self.user.username} | Class {self.student_class}{self.section} | Roll {self.roll_no}"


# ==================================================
# HOMEWORK MODEL  ✅ (DAY 9 CORE)
# ==================================================
class Homework(models.Model):
    """
    Homework Model
    --------------
    - Teacher add karega
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
        ordering = ['due_date']
        verbose_name = 'Homework'
        verbose_name_plural = 'Homeworks'

    def __str__(self):
        return f"{self.title} | Due: {self.due_date}"
