from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.contrib import messages
from datetime import date

from accounts.models import User, StudentProfile
from .models import Attendance


# ======================================================
# 👨‍🏫 TEACHER: MARK ATTENDANCE
# ======================================================
@login_required
def mark_attendance(request):
    """
    Teacher Attendance Mark View
    ----------------------------
    - Sirf TEACHER access
    - Class + section wise students
    - Roll number wise order
    - Duplicate attendance prevent
    """

    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    teacher_profile = getattr(request.user, 'teacher_profile', None)
    if not teacher_profile:
        return HttpResponseForbidden("Teacher profile not found")

    assigned_class = teacher_profile.assigned_class
    assigned_section = teacher_profile.assigned_section

    # 🎓 Students (CLASS + SECTION + ROLL WISE)
    student_profiles = StudentProfile.objects.filter(
        student_class=assigned_class,
        section=assigned_section
    ).select_related('user').order_by('roll_no')

    selected_date = timezone.now().date()

    if request.method == 'POST':
        raw_date = request.POST.get('date')

        # ✅ SAFE date parsing
        if raw_date:
            try:
                selected_date = date.fromisoformat(raw_date)
            except ValueError:
                messages.error(request, "Invalid date format ❌")
                return redirect('mark_attendance')

        saved_count = 0

        for sp in student_profiles:
            status = request.POST.get(f"status_{sp.user.id}")

            if status in ['P', 'A']:
                Attendance.objects.update_or_create(
                    student=sp.user,
                    date=selected_date,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
                saved_count += 1

        messages.success(
            request,
            f"Attendance saved successfully ✅ ({saved_count} students)"
        )
        return redirect('mark_attendance')

    return render(request, 'attendance/mark_attendance.html', {
        'students': student_profiles,
        'date': selected_date,
        'class_name': assigned_class,
        'section': assigned_section
    })


# ======================================================
# 👨‍🎓 STUDENT: VIEW OWN ATTENDANCE
# ======================================================
@login_required
def student_attendance(request):
    """
    Student Attendance View
    -----------------------
    - STUDENT sirf apni attendance dekhe
    - Percentage calculated
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    records = Attendance.objects.filter(
        student=request.user
    ).order_by('-date')

    total_days = records.count()
    present_days = records.filter(status='P').count()

    percentage = round((present_days / total_days) * 100, 2) if total_days else 0

    return render(request, 'attendance/student_attendance.html', {
        'records': records,
        'total_days': total_days,
        'present_days': present_days,
        'percentage': percentage
    })


# ======================================================
# 📊 ADMIN / TEACHER: MONTHLY ATTENDANCE REPORT
# ======================================================
@login_required
def monthly_attendance_report(request):
    """
    Monthly Attendance Report
    -------------------------
    - ADMIN & TEACHER allowed
    - Month / Year based report
    """

    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("Access Denied")

    today = date.today()
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))

    students = User.objects.filter(role='STUDENT').select_related('student_profile')

    report = []

    for student in students:
        qs = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year
        )

        report.append({
            'student': student,
            'present': qs.filter(status='P').count(),
            'absent': qs.filter(status='A').count(),
        })

    return render(request, 'attendance/monthly_report.html', {
        'report': report,
        'month': month,
        'year': year
    })
