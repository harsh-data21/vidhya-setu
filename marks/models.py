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

    name = models.CharField(max_length=100)

    # Subject kis class ka hai
    class_name = models.CharField(
        max_length=2,
        help_text="Class for which subject belongs (e.g. 6, 7, 8)"
    )

    class Meta:
        unique_together = ('name', 'class_name')
        ordering = ['class_name', 'name']
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.name} (Class {self.class_name})"


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
        limit_choices_to={'role': 'STUDENT'},
        related_name="student_marks"
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="marks"
    )

    exam_name = models.CharField(
        max_length=50,
        default="Unit Test",
        help_text="Eg: Unit Test, Mid Term, Final"
    )

    marks_obtained = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    total_marks = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Teacher who uploaded marks
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'TEACHER'},
        related_name="uploaded_marks"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ==================================================
    # Helper Methods
    # ==================================================
    def percentage(self):
        """
        Safely calculate percentage
        """
        if self.marks_obtained is None or not self.total_marks:
            return 0
        return round((self.marks_obtained / self.total_marks) * 100, 2)

    percentage.short_description = "Percentage"

    def grade(self):
        """
        Grade based on percentage
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

    # ==================================================
    # Validation
    # ==================================================
    def clean(self):
        """
        Validation rules
        """

        # Student role validation (extra safety)
        if self.student and getattr(self.student, 'role', None) != 'STUDENT':
            raise ValidationError("Marks can only be assigned to students.")

        # Teacher role validation
        if self.uploaded_by and getattr(self.uploaded_by, 'role', None) != 'TEACHER':
            raise ValidationError("Marks can only be uploaded by a teacher.")

        # Marks logic validation
        if (
            self.marks_obtained is not None
            and self.total_marks is not None
            and self.marks_obtained > self.total_marks
        ):
            raise ValidationError(
                "Obtained marks cannot be greater than total marks."
            )

    def save(self, *args, **kwargs):
        """
        Ensure validation always runs
        """
        self.full_clean()
        super().save(*args, **kwargs)

    # ==================================================
    # Meta Configuration
    # ==================================================
    class Meta:
        verbose_name = "Student Mark"
        verbose_name_plural = "Student Marks"

        # Same student + same subject + same exam duplicate na ho
        unique_together = ('student', 'subject', 'exam_name')

        ordering = ['student__username', 'subject__name']

    def __str__(self):
        return f"{self.student.username} - {self.subject.name} ({self.exam_name})"
