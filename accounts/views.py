from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q
from datetime import datetime

from .models import User, Homework, StudentProfile, Notice


# ==================================================
# HOME PAGE
# ==================================================
def home(request):
    return render(request, 'home.html')


# ==================================================
# LOGIN VIEW
# ==================================================
def login_view(request):

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

        if not username or not password:
            messages.error(request, "All fields are required")
            return redirect('login')

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
# LOGOUT
# ==================================================
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# ==================================================
# DASHBOARDS
# ==================================================
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html')


@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html')


@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")
    return render(request, 'dashboard/dashboard.html')


# ==================================================
# STUDENT REGISTRATION (FINAL)
# ==================================================
@login_required
def student_register(request):

    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Only admin can register students")

    CLASS_CHOICES = ['1','2','3','4','5','6','7','8','9','10','11','12']
    SECTION_CHOICES = ['A','B','C']

    if request.method == "POST":

        first_name = request.POST.get('first_name', '').strip()
        middle_name = request.POST.get('middle_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()

        father_name = request.POST.get('father_name', '').strip()
        mother_name = request.POST.get('mother_name', '').strip()
        contact_number = request.POST.get('contact_number', '').strip()
        address = request.POST.get('address', '').strip()

        dob = request.POST.get('dob')
        admission_number = request.POST.get('admission_number', '').strip()

        student_class = request.POST.get('student_class')
        section = request.POST.get('section')

        if not all([
            first_name, last_name, father_name, mother_name,
            contact_number, address, dob, admission_number,
            student_class, section
        ]):
            messages.error(request, "All fields are required")
            return redirect('student_register')

        dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()

        # password: firstname@year
        temp_password = f"{first_name.lower()}@{dob_obj.year}"

        # username: firstname + lastname + date
        base_username = f"{first_name.lower()}{last_name.lower()}{dob_obj.day}"
        username = base_username
        count = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{count}"
            count += 1

        last_student = StudentProfile.objects.filter(
            student_class=student_class,
            section=section
        ).order_by('-roll_no').first()

        roll_no = last_student.roll_no + 1 if last_student else 1

        user = User.objects.create_user(
            username=username,
            password=temp_password,
            role='STUDENT'
        )

        StudentProfile.objects.create(
            user=user,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            father_name=father_name,
            mother_name=mother_name,
            contact_number=contact_number,
            address=address,
            dob=dob_obj,
            admission_number=admission_number,
            student_class=student_class,
            section=section,
            roll_no=roll_no
        )

        messages.success(
            request,
            f"Student registered successfully | Username: {username} | Temp Password: {temp_password}"
        )
        return redirect('admin_dashboard')

    return render(request, 'register/student_register.html', {
        'classes': CLASS_CHOICES,
        'sections': SECTION_CHOICES
    })


# ==================================================
# STUDENT LIST + SEARCH + FILTER  ✅ (STEP 2)
# ==================================================
@login_required
def student_list(request):

    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("Access Denied")

    students = StudentProfile.objects.select_related('user')

    query = request.GET.get('q')
    if query:
        students = students.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(roll_no__icontains=query) |
            Q(admission_number__icontains=query)
        )

    student_class = request.GET.get('class')
    section = request.GET.get('section')
    fees = request.GET.get('fees')

    if student_class:
        students = students.filter(student_class=student_class)

    if section:
        students = students.filter(section=section)

    if fees == 'paid':
        students = students.filter(fees_paid=True)
    elif fees == 'unpaid':
        students = students.filter(fees_paid=False)

    students = students.order_by('student_class', 'section', 'roll_no')

    return render(request, 'student/student_list.html', {
        'students': students
    })


# ==================================================
# HOMEWORK
# ==================================================
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
        messages.success(request, "Homework added")
        return redirect('teacher_dashboard')

    return render(request, 'teacher/add_homework.html')


@login_required
def view_homework(request):

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    homework = Homework.objects.all().order_by('-created_at')
    return render(request, 'student/view_homework.html', {'homework': homework})


# ==================================================
# NOTICE
# ==================================================
@login_required
def notice_list(request):
    notices = Notice.objects.filter(is_active=True)
    return render(request, 'notice/notice_list.html', {'notices': notices})


# ==================================================
# MANAGE USERS
# ==================================================
@login_required
def manage_users(request):

    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")

    users = User.objects.all().order_by('role')
    return render(request, 'admin/manage_users.html', {'users': users})


# ==================================================
# EDIT USER
# ==================================================
@login_required
def edit_user(request, user_id):

    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST.get('username')
        user.role = request.POST.get('role')
        user.save()
        messages.success(request, "User updated")
        return redirect('manage_users')

    return render(request, 'admin/edit_user.html', {'user_obj': user})


# ==================================================
# TOGGLE USER STATUS
# ==================================================
@login_required
def toggle_user_status(request, user_id):

    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("Access Denied")

    user = get_object_or_404(User, id=user_id)

    if user == request.user:
        messages.error(request, "You cannot disable yourself")
        return redirect('manage_users')

    user.is_active = not user.is_active
    user.save()

    messages.success(request, "User status updated")
    return redirect('manage_users')
