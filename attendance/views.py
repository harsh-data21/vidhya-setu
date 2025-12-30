from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponseForbidden
from datetime import date

from accounts.models import User
from .models import Attendance


# ======================================================
# 👨‍🏫 TEACHER: MARK ATTENDANCE
# ======================================================
@login_required
def mark_attendance(request):
    """
    Teacher Attendance Mark View
    ----------------------------
    - Sirf TEACHER access kar sakta hai
    - Teacher students ki daily attendance mark karta hai
    - Same date par duplicate attendance create nahi hoti
    """

    # 🔐 Role check: sirf TEACHER allowed
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    # ✅ Sirf STUDENT role wale users
    students = User.objects.filter(role='STUDENT')

    # ✅ Default date = aaj (timezone safe)
    selected_date = timezone.now().date()

    # -------------------------
    # FORM SUBMIT (POST REQUEST)
    # -------------------------
    if request.method == 'POST':

        # Agar template se date bheji gayi ho
        selected_date = request.POST.get('date') or selected_date

        # Har student ke liye attendance process
        for student in students:
            # input ka name = student.id
            # value = 'P' (Present) ya 'A' (Absent)
            status = request.POST.get(str(student.id))

            # Sirf tab save kare jab status mila ho
            if status:
                Attendance.objects.update_or_create(
                    student=student,     # kis student ki
                    date=selected_date,  # kis date ki
                    defaults={
                        'status': status,
                        'marked_by': request.user  # kaun teacher ne mark ki
                    }
                )

        # Attendance mark hone ke baad teacher dashboard
        return redirect('teacher_dashboard')

    # -------------------------
    # PAGE LOAD (GET REQUEST)
    # -------------------------
    return render(request, 'attendance/mark_attendance.html', {
        'students': students,      # students list
        'date': selected_date      # date input ke liye
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

    # 🔐 Role check
    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    # ✅ Sirf apni attendance records
    records = Attendance.objects.filter(student=request.user)

    # 📊 Total days
    total_days = records.count()

    # 📊 Present days
    present_days = records.filter(status='P').count()

    # 📈 Attendance percentage
    percentage = 0
    if total_days > 0:
        percentage = round((present_days / total_days) * 100, 2)

    return render(request, 'attendance/student_attendance.html', {
        'records': records.order_by('-date'),  # latest first
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

    # 🔐 Role check
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("Access Denied")

    # ✅ Sabhi students
    students = User.objects.filter(role='STUDENT')

    # URL params (?month=7&year=2025)
    month = request.GET.get('month')
    year = request.GET.get('year')

    # Default = current month/year
    today = date.today()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    report = []

    # Har student ka monthly data
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
