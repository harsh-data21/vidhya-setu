from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden

from .models import User, Homework, StudentProfile, Notice


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
    Handles user login
    - Username & password authenticate
    - Role based dashboard redirect
    """

    # Already logged-in user
    if request.user.is_authenticated:
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        elif request.user.role == 'TEACHER':
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user:
            if not user.is_active:
                messages.error(request, "Your account is inactive")
                return redirect('login')

            login(request, user)

            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'TEACHER':
                return redirect('teacher_dashboard')
            else:
                return redirect('student_dashboard')

        messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ==================================================
# LOGOUT VIEW
# ==================================================
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ==================================================
# ROLE BASED DASHBOARDS
# ==================================================
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


# ==================================================
# STUDENT REGISTRATION (AUTO ROLL)
# ==================================================
def student_register(request):
    """
    Student Registration
    - Roll number auto-generated (class + section wise)
    """

    CLASS_CHOICES = ['1','2','3','4','5','6','7','8','9','10','11','12']

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        father_name = request.POST.get('father_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        student_class = request.POST.get('student_class')
        section = request.POST.get('section')

        if not all([username, password, father_name, contact_number]):
            messages.error(request, "All fields are required")
            return redirect('student_register')

        if not contact_number.isdigit() or len(contact_number) < 10:
            messages.error(request, "Enter valid contact number")
            return redirect('student_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('student_register')

        last_student = StudentProfile.objects.filter(
            student_class=student_class,
            section=section
        ).order_by('-roll_no').first()

        roll_no = last_student.roll_no + 1 if last_student else 1

        user = User.objects.create_user(
            username=username,
            password=password,
            role='STUDENT'
        )

        StudentProfile.objects.create(
            user=user,
            father_name=father_name,
            contact_number=contact_number,
            student_class=student_class,
            section=section,
            roll_no=roll_no
        )

        messages.success(
            request,
            f"Student registered successfully. Roll No: {roll_no}"
        )
        return redirect('login')

    return render(request, 'register/student_register.html', {
        'classes': CLASS_CHOICES
    })


# ==================================================
# HOMEWORK MODULE
# ==================================================
@login_required
def add_homework(request):
    """
    Teacher homework add karega
    """

    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    if request.method == "POST":
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date = request.POST.get('due_date')

        if not all([title, description, due_date]):
            messages.error(request, "All fields are required")
            return redirect('add_homework')

        Homework.objects.create(
            teacher=request.user,
            title=title,
            description=description,
            due_date=due_date
        )

        messages.success(request, "Homework added successfully")
        return redirect('teacher_dashboard')

    return render(request, 'teacher/add_homework.html')


@login_required
def view_homework(request):
    """
    Student homework view karega
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    homework = Homework.objects.all().order_by('-created_at')

    return render(request, 'student/view_homework.html', {
        'homework': homework
    })


# ==================================================
# NOTICE MODULE  ✅ FINAL
# ==================================================
@login_required
def notice_list(request):
    """
    Student & Teacher notices view karenge
    """

    notices = Notice.objects.filter(is_active=True).order_by('-created_at')

    return render(request, 'notice/notice_list.html', {
        'notices': notices
    })
