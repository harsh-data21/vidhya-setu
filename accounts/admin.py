from django.contrib import admin
from .models import (
    User,
    TeacherProfile,
    StudentProfile,
    Homework,
    Notice
)


# ==================================================
# USER ADMIN
# ==================================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for Custom User model
    """

    list_display = (
        'username',
        'email',
        'role',
        'is_staff',
        'is_active',
    )

    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )

    ordering = ('username',)


# ==================================================
# TEACHER PROFILE ADMIN
# ==================================================
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for TeacherProfile
    """

    list_display = (
        'user',
        'designation',
        'subject',
        'assigned_class',
        'assigned_section',
        'phone',
    )

    list_filter = (
        'designation',
        'assigned_class',
        'assigned_section',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'subject',
    )

    ordering = (
        'assigned_class',
        'assigned_section',
        'user__username',
    )


# ==================================================
# STUDENT PROFILE ADMIN
# ==================================================
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for StudentProfile
    """

    list_display = (
        'user',
        'father_name',
        'contact_number',
        'student_class',
        'section',
        'roll_no',
    )

    list_filter = (
        'student_class',
        'section',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'father_name',
        'contact_number',
        'roll_no',
    )

    ordering = (
        'student_class',
        'section',
        'roll_no',
    )


# ==================================================
# HOMEWORK ADMIN
# ==================================================
@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    """
    Admin configuration for Homework
    """

    list_display = (
        'title',
        'teacher',
        'due_date',
        'created_at',
    )

    list_filter = (
        'due_date',
        'teacher',
    )

    search_fields = (
        'title',
        'teacher__username',
    )

    ordering = ('due_date',)


# ==================================================
# NOTICE ADMIN  ✅ (MISSING PART – NOW ADDED)
# ==================================================
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Notice
    """

    list_display = (
        'title',
        'created_by',
        'created_at',
        'is_active',
    )

    list_filter = (
        'is_active',
        'created_at',
    )

    search_fields = (
        'title',
        'message',
        'created_by__username',
    )

    ordering = ('-created_at',)


# ==================================================
# ADMIN PANEL BRANDING
# ==================================================
admin.site.site_header = "Vidhya Setu Administration"
admin.site.site_title = "Vidhya Setu Admin Portal"
admin.site.index_title = "Welcome to Vidhya Setu Admin Panel"
