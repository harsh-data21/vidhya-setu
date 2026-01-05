from django.contrib import admin
from .models import Subject, StudentMark


# ==================================================
# 📚 SUBJECT ADMIN CONFIGURATION
# ==================================================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin panel me subjects ko manage karne ke liye
    """

    list_display = (
        'id',
        'name',
        'class_name',
    )

    list_filter = (
        'class_name',
    )

    search_fields = (
        'name',
    )

    ordering = (
        'class_name',
        'name',
    )


# ==================================================
# 📝 STUDENT MARK ADMIN CONFIGURATION
# ==================================================
@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    """
    Admin panel me student-wise marks dekhne / manage karne ke liye
    (Mostly read-only for safety)
    """

    # -----------------------------
    # Table columns
    # -----------------------------
    list_display = (
        'student',
        'subject',
        'exam_name',
        'marks_obtained',
        'total_marks',
        'percentage_display',
        'grade_display',
        'uploaded_by',
    )

    # -----------------------------
    # Filters (right side)
    # -----------------------------
    list_filter = (
        'exam_name',
        'subject__class_name',
        'subject',
    )

    # -----------------------------
    # Search bar
    # -----------------------------
    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'subject__name',
    )

    # -----------------------------
    # Ordering
    # -----------------------------
    ordering = (
        'student__username',
        'subject__name',
        'exam_name',
    )

    # -----------------------------
    # Read-only fields (SAFE ADMIN)
    # -----------------------------
    readonly_fields = (
        'student',
        'subject',
        'exam_name',
        'marks_obtained',
        'total_marks',
        'uploaded_by',
        'created_at',
        'updated_at',
    )

    # -----------------------------
    # Custom display methods
    # -----------------------------
    def percentage_display(self, obj):
        return f"{obj.percentage()} %"
    percentage_display.short_description = "Percentage"

    def grade_display(self, obj):
        return obj.grade()
    grade_display.short_description = "Grade"
