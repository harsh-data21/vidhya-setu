from django.urls import path
from .views import (
    home,
    login_view,
    logout_view,
    admin_dashboard,
    teacher_dashboard,
    student_dashboard,
    add_homework,
    view_homework,
)

# ==================================================
# ACCOUNTS APP URL CONFIGURATION
# ==================================================
urlpatterns = [

    # --------------------
    # HOME & AUTHENTICATION
    # --------------------
    path('', home, name='home'),                 # Public home page
    path('login/', login_view, name='login'),    # Login page
    path('logout/', logout_view, name='logout'), # Logout action


    # --------------------
    # ROLE-BASED DASHBOARDS
    # --------------------
    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),  # Admin dashboard (ADMIN only)

    path(
        'teacher-dashboard/',
        teacher_dashboard,
        name='teacher_dashboard'
    ),  # Teacher dashboard (TEACHER only)

    path(
        'student-dashboard/',
        student_dashboard,
        name='student_dashboard'
    ),  # Student dashboard (STUDENT only)


    # --------------------
    # HOMEWORK MODULE
    # --------------------
    path(
        'teacher/add-homework/',
        add_homework,
        name='add_homework'
    ),  # Teacher adds homework

    path(
        'student/homework/',
        view_homework,
        name='view_homework'
    ),  # Student views homework
]
