from django.contrib import admin
from .models import Subject, StudentMark


# -----------------------------
# Subject Admin Configuration
# -----------------------------
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Admin panel me subjects ko manage karne ke liye
    """
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


# -----------------------------
# StudentMark Admin Configuration
# -----------------------------
@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):
    """
    Admin panel me student-wise marks manage karne ke liye
    """

    # -----------------------------
    # Table columns
    # -----------------------------
    list_display = (
        'student',
        'subject',
        'marks_obtained',
        'max_marks',
        'percentage_display',
        'grade_display',
        'uploaded_by',
        'created_at',
    )

    # -----------------------------
    # Filters (right side)
    # -----------------------------
    list_filter = (
        'subject',
        'uploaded_by',
    )

    # -----------------------------
    # Search bar
    # -----------------------------
    search_fields = (
        'student__username',
        'subject__name',
    )

    # -----------------------------
    # Read-only fields
    # -----------------------------
    readonly_fields = (
        'created_at',
        'updated_at',
        'percentage_display',
        'grade_display',
    )

    # -----------------------------
    # Ordering
    # -----------------------------
    ordering = ('student__username', 'subject__name')

    # -----------------------------
    # Custom display methods
    # -----------------------------
    def percentage_display(self, obj):
        return f"{obj.percentage()} %"
    percentage_display.short_description = "Percentage"

    def grade_display(self, obj):
        return obj.grade()
    grade_display.short_description = "Grade"
