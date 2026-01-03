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
        'id',
        'user',
        'get_first_name',
        'get_last_name',
        'student_class',
        'section',
        'roll_no',
    )

    list_filter = (
        'student_class',
        'section',
    )

    ordering = (
        'student_class',
        'section',
        'roll_no',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'roll_no',
    )

    # -------- User fields helpers --------
    def get_first_name(self, obj):
        return obj.user.first_name
    get_first_name.short_description = 'First Name'

    def get_last_name(self, obj):
        return obj.user.last_name
    get_last_name.short_description = 'Last Name'


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
# NOTICE ADMIN
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
