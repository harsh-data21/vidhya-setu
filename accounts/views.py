from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Homework


# ==================================================
# HOME PAGE
# ==================================================
def home(request):
    """
    Public home page
    - Login se pehle sab users ke liye accessible
    """
    return render(request, 'home.html')


# ==================================================
# LOGIN VIEW
# ==================================================
def login_view(request):
    """
    Handles user login:
    - Username & password authenticate karta hai
    - Role ke basis par dashboard redirect karta hai
    """

    # Agar user already logged in hai → direct dashboard bhejo
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'TEACHER':
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')

    # Login form submit hone par
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django built-in authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Extra security: inactive user login na kare
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect('login')

            # Login success
            login(request, user)

            # Role-based dashboard redirect
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'TEACHER':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    # GET request → login page show
    return render(request, 'login.html')


# ==================================================
# LOGOUT VIEW
# ==================================================
@login_required
def logout_view(request):
    """
    User logout:
    - Session clear karta hai
    - Login page par redirect karta hai
    """
    logout(request)
    return redirect('login')


# ==================================================
# ROLE BASED DASHBOARDS (SECURE)
# ==================================================

@login_required
def admin_dashboard(request):
    """
    Admin dashboard:
    - Sirf ADMIN role allowed
    """
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")

    return render(request, 'dashboard/dashboard.html', {
        'role': 'Admin'
    })


@login_required
def teacher_dashboard(request):
    """
    Teacher dashboard:
    - Sirf TEACHER role allowed
    """
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    return render(request, 'dashboard/dashboard.html', {
        'role': 'Teacher'
    })


@login_required
def student_dashboard(request):
    """
    Student dashboard:
    - Sirf STUDENT role allowed
    """
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    return render(request, 'dashboard/dashboard.html', {
        'role': 'Student'
    })


# ==================================================
# DAY 5 / DAY 6 : HOMEWORK MODULE
# ==================================================

# --------------------
# TEACHER: ADD HOMEWORK
# --------------------
@login_required
def add_homework(request):
    """
    Homework add karne ka view:
    - Sirf TEACHER homework add kar sakta hai
    - Homework teacher se linked hota hai
    """

    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    if request.method == "POST":
        Homework.objects.create(
            teacher=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            due_date=request.POST.get('due_date')
        )

        messages.success(request, "Homework added successfully")
        return redirect('teacher_dashboard')

    # GET request → homework add form
    return render(request, 'teacher/add_homework.html')


# --------------------
# STUDENT: VIEW HOMEWORK
# --------------------
@login_required
def view_homework(request):
    """
    Homework view karne ka view:
    - Sirf STUDENT homework dekh sakta hai
    - Latest homework sabse upar show hota hai
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    homework = Homework.objects.all().order_by('-created_at')

    return render(request, 'student/view_homework.html', {
        'homework': homework
    })
