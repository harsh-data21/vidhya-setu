from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date

from accounts.models import User
from .models import Attendance


# ======================================================
# 👨‍🏫 TEACHER: MARK ATTENDANCE
# ======================================================
@login_required
def mark_attendance(request):
    # ❌ Agar user teacher nahi hai to login page par bhej do
    if request.user.role != 'TEACHER':
        return redirect('login')

    # ✅ Sirf STUDENT role wale users nikaalo
    students = User.objects.filter(role='STUDENT')

    # ✅ Aaj ki date (timezone safe)
    today = timezone.now().date()

    # -------------------------
    # FORM SUBMIT (POST REQUEST)
    # -------------------------
    if request.method == 'POST':
        for student in students:
            # Template se aane wala status (P / A)
            # checkbox / radio ka name = student.id
            status = request.POST.get(str(student.id))

            # Agar status mila tabhi entry banao / update karo
            if status:
                Attendance.objects.update_or_create(
                    student=student,   # kis student ki attendance
                    date=today,        # kis date ki
                    defaults={
                        'status': status,          # Present / Absent
                        'marked_by': request.user  # kis teacher ne mark ki
                    }
                )

        # Attendance mark hone ke baad teacher dashboard
        return redirect('teacher_dashboard')

    # -------------------------
    # PAGE LOAD (GET REQUEST)
    # -------------------------
    return render(request, 'attendance/mark_attendance.html', {
        'students': students,  # student list template ko bhejna
        'date': today          # aaj ki date show karne ke liye
    })


# ======================================================
# 👨‍🎓 STUDENT: VIEW OWN ATTENDANCE
# ======================================================
@login_required
def student_attendance(request):
    # ❌ Agar student nahi hai to access deny
    if request.user.role != 'STUDENT':
        return render(request, '403.html')

    # ✅ Student sirf apni attendance dekh sakta hai
    records = Attendance.objects.filter(student=request.user)

    # 📊 Total attendance days
    total_days = records.count()

    # 📊 Present days (model me 'P' short code use hua hai)
    present_days = records.filter(status='P').count()

    # 📈 Attendance percentage calculate
    percentage = 0
    if total_days > 0:
        percentage = round((present_days / total_days) * 100, 2)

    return render(request, 'attendance/student_attendance.html', {
        'records': records.order_by('-date'),  # latest date upar
        'total_days': total_days,
        'present_days': present_days,
        'percentage': percentage
    })


# ======================================================
# 📊 ADMIN / TEACHER: MONTHLY ATTENDANCE REPORT
# ======================================================
@login_required
def monthly_attendance_report(request):
    # ❌ Sirf ADMIN ya TEACHER allowed
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return render(request, '403.html')

    # ✅ Sab students nikaalo
    students = User.objects.filter(role='STUDENT')

    # URL se month aur year lo (?month=7&year=2025)
    month = request.GET.get('month')
    year = request.GET.get('year')

    # Agar month/year nahi diya to current month/year
    today = date.today()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    report = []

    # Har student ka monthly data banao
    for student in students:
        present_count = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year,
            status='P'   # Present
        ).count()

        absent_count = Attendance.objects.filter(
            student=student,
            date__month=month,
            date__year=year,
            status='A'   # Absent
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
