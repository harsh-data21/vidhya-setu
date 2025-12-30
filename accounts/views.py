from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import Homework


# --------------------
# HOME PAGE
# --------------------
def home(request):
    return render(request, 'home.html')


# --------------------
# LOGIN VIEW
# --------------------
def login_view(request):

    # Agar user already login hai
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'TEACHER':
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:

            # IMPORTANT CHECK
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect('login')

            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'TEACHER':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# --------------------
# LOGOUT VIEW
# --------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# --------------------
# ROLE BASED DASHBOARDS (SECURE)
# --------------------
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Admin'})


@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Teacher'})


@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html', {'role': 'Student'})


# --------------------
# DAY 5 : HOMEWORK
# --------------------
@login_required
def add_homework(request):
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

    # 👇 YE LINE IMPORTANT HAI
    return render(request, 'teacher/add_homework.html')


@login_required
def view_homework(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    homework = Homework.objects.all().order_by('-created_at')
    return render(request, 'student/view_homework.html', {'homework': homework})
