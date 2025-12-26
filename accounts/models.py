from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


UserModel = settings.AUTH_USER_MODEL


class TeacherProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

class StudentProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    roll_no = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
