from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import User


# --------------------
# Subject Model
# --------------------
class Subject(models.Model):
    """
    School subjects like:
    Maths, English, Science, etc.
    """
    name = models.CharField(
        max_length=100,
        unique=True   # same subject dobara create na ho
    )

    def __str__(self):
        return self.name


# --------------------
# Student Marks Model
# --------------------
class StudentMark(models.Model):
    """
    Student ke subject-wise marks store karne ke liye
    Teacher decide karta hai:
    - Exam kitne marks ka hai
    - Student ne kitne marks obtain kiye
    """

    # --------------------
    # Relations
    # --------------------
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='marks'
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='student_marks'
    )

    # --------------------
    # Marks Info
    # --------------------
    marks_obtained = models.PositiveIntegerField(
        help_text="Marks obtained by student"
    )

    max_marks = models.PositiveIntegerField(
        help_text="Total marks of the exam (e.g. 70, 80, 100)"
    )

    # --------------------
    # Meta Info
    # --------------------
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'TEACHER'},
        related_name='uploaded_marks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Ek student + subject ka ek hi marks record
        unique_together = ('student', 'subject')
        ordering = ['student__username', 'subject__name']

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"

    # --------------------
    # Helper Methods
    # --------------------
    def percentage(self):
        """
        Student ka percentage calculate karta hai
        """
        if self.max_marks > 0:
            return round((self.marks_obtained / self.max_marks) * 100, 2)
        return 0

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

    def clean(self):
        """
        Validation:
        - Obtained marks total marks se zyada nahi ho sakte
        """
        if self.marks_obtained > self.max_marks:
            raise ValidationError(
                "Obtained marks cannot be greater than total marks"
            )
