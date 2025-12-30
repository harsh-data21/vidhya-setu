from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import date

from accounts.models import User
from .models import Attendance


# =========================
# TEACHER: MARK ATTENDANCE
# =========================
@login_required
def mark_attendance(request):
    # Sirf TEACHER access
    if request.user.role != 'TEACHER':
        return redirect('login')

    students = User.objects.filter(role='STUDENT')
    today = timezone.now().date()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(str(student.id))
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={
                        'status': status,
                        'marked_by': request.user
                    }
                )
        return redirect('teacher_dashboard')

    return render(request, 'attendance/mark_attendance.html', {
        'students': students,
        'date': today
    })


# =========================
# STUDENT: VIEW ATTENDANCE
# =========================
@login_required
def student_attendance(request):
    if request.user.role != 'STUDENT':
        return render(request, '403.html')

    records = Attendance.objects.filter(student=request.user)

    total_days = records.count()
    present_days = records.filter(status='PRESENT').count()

    percentage = 0
    if total_days > 0:
        percentage = round((present_days / total_days) * 100, 2)

    return render(request, 'attendance/student_attendance.html', {
        'records': records.order_by('-date'),
        'total_days': total_days,
        'present_days': present_days,
        'percentage': percentage
    })



# =========================
# TEACHER / ADMIN: MONTHLY REPORT
# =========================
@login_required
def monthly_attendance_report(request):
    # Sirf ADMIN ya TEACHER
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return render(request, '403.html')

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
            status='PRESENT'
        ).count()

        absent_count = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year,
            status='ABSENT'
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
