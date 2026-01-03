from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, TeacherProfile, StudentProfile


# ==================================================
# SIGNAL: CREATE PROFILE AFTER USER CREATION
# ==================================================
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    🔹 Jab naya User create hota hai
    🔹 Uske role ke hisaab se profile auto-create hoti hai
    """

    # ❗ Sirf first time user create hone par
    if not created:
        return

    # -------- TEACHER PROFILE --------
    if instance.role == 'TEACHER':
        TeacherProfile.objects.get_or_create(
            user=instance,
            defaults={
                "subject": "Not Assigned"
            }
        )

    # -------- STUDENT PROFILE --------
    elif instance.role == 'STUDENT':
        StudentProfile.objects.get_or_create(
            user=instance
        )
