from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from accounts.models import User, StudentProfile

# Fees app OPTIONAL hai – isliye safe import
try:
    from fees.models import StudentFee
except ImportError:
    StudentFee = None


# ==================================================
# 🧑‍💼 ADMIN DASHBOARD
# ==================================================
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN':
        return HttpResponseForbidden("You are not allowed to access this page.")

    # ---------- REAL DB COUNTS ----------
    total_students = StudentProfile.objects.count()
    total_teachers = User.objects.filter(role='TEACHER').count()

    # Fees (safe handling)
    if StudentFee:
        total_fees = StudentFee.objects.count()
        pending_fees = StudentFee.objects.filter(status='PENDING').count()
    else:
        total_fees = 0
        pending_fees = 0

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_fees': total_fees,
        'pending_fees': pending_fees,
    }

    return render(request, 'dashboard/admin_dashboard.html', context)


# ==================================================
# 👨‍🏫 TEACHER DASHBOARD
# ==================================================
@login_required
def teacher_dashboard(request):
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("You are not allowed to access this page.")

    return render(request, 'dashboard/teacher_dashboard.html')


@login_required
def teacher_attendance(request):
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden()

    return render(request, 'dashboard/teacher_attendance.html')


@login_required
def teacher_marks(request):
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden()

    return render(request, 'dashboard/teacher_marks.html')


# ==================================================
# 🎒 STUDENT DASHBOARD
# ==================================================
@login_required
def student_dashboard(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("You are not allowed to access this page.")

    return render(request, 'dashboard/student_dashboard.html')


@login_required
def student_attendance(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden()

    return render(request, 'dashboard/student_attendance.html')


@login_required
def student_marks(request):
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden()

    return render(request, 'dashboard/student_marks.html')
