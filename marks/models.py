from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


# ==================================================
# SUBJECT MODEL
# ==================================================
class Subject(models.Model):
    """
    School subjects like:
    Maths, English, Science, etc.
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


# ==================================================
# STUDENT MARK MODEL
# ==================================================
class StudentMark(models.Model):
    """
    Stores marks of a student for a subject
    """

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    marks_obtained = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    total_marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # --------------------
    # Helper Methods
    # --------------------
    def percentage(self):
        """
        Safely calculate percentage
        (Admin GET request safe)
        """

        if self.marks_obtained is None or self.total_marks is None:
            return 0

        if self.total_marks == 0:
            return 0

        return round((self.marks_obtained / self.total_marks) * 100, 2)

    percentage.short_description = "Percentage"

    def grade(self):
        """
        Percentage ke base par grade return karta hai
        """

        percent = self.percentage()

        if percent >= 90:
            return "A+"
        elif percent >= 75:
            return "A"
        elif percent >= 60:
            return "B"
        elif percent >= 40:
            return "C"
        else:
            return "Fail"

    # --------------------
    # Validation
    # --------------------
    def clean(self):
        """
        Validation:
        - Obtained marks total marks se zyada nahi ho sakte
        """

        if (
            self.marks_obtained is not None
            and self.total_marks is not None
            and self.marks_obtained > self.total_marks
        ):
            raise ValidationError(
                "Obtained marks cannot be greater than total marks"
            )

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"
