from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render

from accounts.models import User, StudentProfile

# Fees app OPTIONAL hai – safe import
try:
    from fees.models import StudentFee
except ImportError:
    StudentFee = None


# ==================================================
# 🧑‍💼 ADMIN DASHBOARD
# ==================================================
@login_required
def admin_dashboard(request):
    if getattr(request.user, 'role', None) != 'ADMIN':
        return HttpResponseForbidden("You are not allowed to access this page.")

    total_students = StudentProfile.objects.count()
    total_teachers = User.objects.filter(role='TEACHER').count()

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
# 📊 ADMIN: MONTHLY REPORT (FIX for NoReverseMatch)
# ==================================================
@login_required
def monthly_report(request):
    if getattr(request.user, 'role', None) != 'ADMIN':
        return HttpResponseForbidden("You are not allowed to access this page.")

    return render(request, 'dashboard/monthly_report.html')


# ==================================================
# 👨‍🏫 TEACHER DASHBOARD
# ==================================================
@login_required
def teacher_dashboard(request):
    if getattr(request.user, 'role', None) != 'TEACHER':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'dashboard/teacher_dashboard.html')


@login_required
def teacher_attendance(request):
    if getattr(request.user, 'role', None) != 'TEACHER':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'attendance/mark_attendance.html')


@login_required
def teacher_marks(request):
    if getattr(request.user, 'role', None) != 'TEACHER':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'marks/upload_marks.html')


# ==================================================
# 🎒 STUDENT DASHBOARD
# ==================================================
@login_required
def student_dashboard(request):
    if getattr(request.user, 'role', None) != 'STUDENT':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'dashboard/student_dashboard.html')


@login_required
def student_attendance(request):
    if getattr(request.user, 'role', None) != 'STUDENT':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'attendance/student_attendance.html')


@login_required
def student_marks(request):
    if getattr(request.user, 'role', None) != 'STUDENT':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'marks/my_marks.html')


@login_required
def my_fees(request):
    if getattr(request.user, 'role', None) != 'STUDENT':
        return HttpResponseForbidden("Access denied.")

    return render(request, 'student/my_fees.html')
