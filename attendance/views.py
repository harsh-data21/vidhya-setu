from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import date

from accounts.models import User
from .models import Attendance


# ======================================================
# 👨‍🏫 TEACHER: MARK ATTENDANCE (CLASS-WISE FINAL)
# ======================================================
@login_required
def mark_attendance(request):
    """
    Teacher Attendance Mark View (FINAL)
    ------------------------------------
    - Sirf TEACHER access kar sakta hai
    - Teacher sirf apni assigned class/section ke students dekhega
    - Same date par duplicate attendance create nahi hoti
    """

    # 🔐 Role check
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    # 🔗 Teacher profile se assigned class & section
    teacher_profile = request.user.teacher_profile
    assigned_class = teacher_profile.assigned_class
    assigned_section = teacher_profile.assigned_section

    # 🎯 Sirf usi class/section ke students
    students = User.objects.filter(
        role='STUDENT',
        student_profile__student_class=assigned_class,
        student_profile__section=assigned_section
    ).select_related('student_profile')

    # 📅 Default date = aaj
    selected_date = timezone.now().date()

    # -------------------------
    # FORM SUBMIT (POST REQUEST)
    # -------------------------
    if request.method == 'POST':

        selected_date = request.POST.get('date') or selected_date

        for student in students:
            # input name = student.id
            status = request.POST.get(str(student.id))

            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=selected_date,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )

        return redirect('teacher_dashboard')

    # -------------------------
    # PAGE LOAD (GET REQUEST)
    # -------------------------
    return render(request, 'attendance/mark_attendance.html', {
        'students': students,
        'date': selected_date,
        'class': assigned_class,
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
    - STUDENT sirf apni hi attendance dekh sakta hai
    - Attendance percentage calculate hoti hai
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    records = Attendance.objects.filter(student=request.user)

    total_days = records.count()
    present_days = records.filter(status='P').count()

    percentage = 0
    if total_days > 0:
        percentage = round((present_days / total_days) * 100, 2)

    return render(request, 'attendance/student_attendance.html', {
        'records': records.order_by('-date'),
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
    - ADMIN aur TEACHER dekh sakte hain
    - Month / Year ke basis par report generate hoti hai
    """

    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("Access Denied")

    students = User.objects.filter(role='STUDENT')

    month = request.GET.get('month')
    year = request.GET.get('year')

    today = date.today()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    report = []

    for student in students:
        present_count = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year,
            status='P'
        ).count()

        absent_count = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year,
            status='A'
        ).count()

        report.append({
            'student': student,
            'present': present_count,
            'absent': absent_count,
        })

    return render(request, 'attendance/monthly_report.html', {
        'report': report,
        'month': month,
        'year': year
    })
