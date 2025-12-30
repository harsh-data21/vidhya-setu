from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import User, TeacherProfile, StudentProfile


# ==================================================
# SIGNAL: CREATE PROFILE AFTER USER CREATION
# ==================================================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    🔹 Jab naya User create hota hai
    🔹 Uske role ke hisaab se profile auto-create hoti hai
    """

    # Sirf naya user create hone par chale
    if created:

        # Agar role TEACHER hai → TeacherProfile banao
        if instance.role == 'TEACHER':
            TeacherProfile.objects.create(
                user=instance,
                subject="Not Assigned"   # default value
            )

        # Agar role STUDENT hai → StudentProfile banao
        elif instance.role == 'STUDENT':
            StudentProfile.objects.create(
                user=instance,
                roll_no=f"ROLL-{instance.id}"  # auto roll number
            )


# ==================================================
# SIGNAL: SAVE PROFILE WHEN USER IS SAVED
# ==================================================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    """
    🔹 Jab User save hota hai
    🔹 Related profile bhi save ho jaata hai
    """

    if instance.role == 'TEACHER' and hasattr(instance, 'teacher_profile'):
        instance.teacher_profile.save()

    elif instance.role == 'STUDENT' and hasattr(instance, 'student_profile'):
        instance.student_profile.save()
