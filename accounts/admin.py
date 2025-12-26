from django.contrib import admin
from .models import User, TeacherProfile, StudentProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role',)
    search_fields = ('username', 'email')


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'phone')
    search_fields = ('user__username', 'subject')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'phone')
    search_fields = ('user__username', 'roll_no')


admin.site.site_header = "Vidhya Setu Administration"
admin.site.site_title = "Vidhya Setu Admin"
admin.site.index_title = "Welcome to Vidhya Setu Admin Panel"

