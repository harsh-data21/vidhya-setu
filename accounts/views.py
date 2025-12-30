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
    """
    return render(request, 'home.html')


# ==================================================
# LOGIN VIEW
# ==================================================
def login_view(request):
    """
    - User login handle karta hai
    - Role ke basis par dashboard redirect
    """

    # Agar user already login hai → direct dashboard
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'TEACHER':
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')

    # Login form submit
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django authentication
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # Extra safety: inactive user login na kare
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect('login')

            # Login success
            login(request, user)

            # Role-based redirect
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'TEACHER':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ==================================================
# LOGOUT VIEW
# ==================================================
@login_required
def logout_view(request):
    """
    User logout
    """
    logout(request)
    return redirect('login')


# ==================================================
# ROLE BASED DASHBOARDS (SECURE)
# ==================================================
@login_required
def admin_dashboard(request):
    """
    Admin dashboard
    """
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Admin'})


@login_required
def teacher_dashboard(request):
    """
    Teacher dashboard
    """
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Teacher'})


@login_required
def student_dashboard(request):
    """
    Student dashboard
    """
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Student'})


# ==================================================
# DAY 5 / DAY 6 : HOMEWORK MODULE
# ==================================================

# --------------------
# TEACHER: ADD HOMEWORK
# --------------------
@login_required
def add_homework(request):
    """
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

    # Homework add form
    return render(request, 'teacher/add_homework.html')


# --------------------
# STUDENT: VIEW HOMEWORK
# --------------------
@login_required
def view_homework(request):
    """
    - Sirf STUDENT homework dekh sakta hai
    - Latest homework upar dikhaya jaata hai
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    homework = Homework.objects.all().order_by('-created_at')

    return render(request, 'student/view_homework.html', {
        'homework': homework
    })
