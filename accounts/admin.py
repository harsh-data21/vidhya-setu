from django.contrib import admin
from .models import User, TeacherProfile, StudentProfile, Homework


# ==================================================
# USER ADMIN
# ==================================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin configuration for Custom User model
    - Username, email, role dikhata hai
    - Role ke basis par filter
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
    - Teacher ki designation, subject, class assignment
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
    - Same name students supported
    - Father name + contact number visible
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
    - Teacher wise homework tracking
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
# ADMIN PANEL BRANDING
# ==================================================
admin.site.site_header = "Vidhya Setu Administration"
admin.site.site_title = "Vidhya Setu Admin Portal"
admin.site.index_title = "Welcome to Vidhya Setu Admin Panel"
