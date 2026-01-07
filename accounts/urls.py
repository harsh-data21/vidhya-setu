from django.urls import path, include

from .views import (
    # Home & Auth
    home,
    login_view,
    logout_view,

    # Student
    student_register,
    student_list,

    # Homework
    add_homework,
    view_homework,

    # Notice
    notice_list,

    # Manage Users
    manage_users,
    toggle_user_status,
    edit_user,
)

urlpatterns = [

    # ==================================================
    # 🏠 HOME & AUTH
    # ==================================================
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # ==================================================
    # 🎓 STUDENTS
    # ==================================================
    path('register/student/', student_register, name='student_register'),
    path('students/', student_list, name='student_list'),

    # ==================================================
    # 📚 HOMEWORK
    # ==================================================
    path('teacher/add-homework/', add_homework, name='add_homework'),
    path('student/homework/', view_homework, name='view_homework'),

    # ==================================================
    # 📢 NOTICE
    # ==================================================
    path('notices/', notice_list, name='notice_list'),

    # ==================================================
    # 💰 FEES MODULE
    # ==================================================
    path('fees/', include('fees.urls')),

    # ==================================================
    # 👥 MANAGE USERS (CUSTOM ADMIN)
    # ==================================================
    path('manage-users/', manage_users, name='manage_users'),
    path('user/<int:user_id>/toggle/', toggle_user_status, name='toggle_user'),
    path('user/<int:user_id>/edit/', edit_user, name='edit_user'),
]
