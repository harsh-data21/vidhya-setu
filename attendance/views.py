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
    """
    Ye view TEACHER ko students ki daily attendance mark karne deta hai.
    """

    # ❌ Agar user TEACHER nahi hai to login page par redirect
    if request.user.role != 'TEACHER':
        return redirect('login')

    # ✅ Sirf STUDENT role wale users fetch karo
    students = User.objects.filter(role='STUDENT')

    # ✅ Timezone-safe aaj ki date
    today = timezone.now().date()

    # -------------------------
    # FORM SUBMIT (POST REQUEST)
    # -------------------------
    if request.method == 'POST':

        # Har student ke liye attendance process karo
        for student in students:
            # Template se aane wala status
            # input ka name = student.id
            # value = 'P' ya 'A'
            status = request.POST.get(str(student.id))

            # Agar status mila tabhi database me save karo
            if status:
                Attendance.objects.update_or_create(
                    student=student,   # kis student ki attendance
                    date=today,        # kis date ki
                    defaults={
                        'status': status,          # Present / Absent
                        'marked_by': request.user  # kaun teacher ne mark ki
                    }
                )

        # Attendance mark hone ke baad teacher dashboard par bhej do
        return redirect('teacher_dashboard')

    # -------------------------
    # PAGE LOAD (GET REQUEST)
    # -------------------------
    return render(request, 'attendance/mark_attendance.html', {
        'students': students,  # students list template ko dene ke liye
        'date': today          # aaj ki date show karne ke liye
    })


# ======================================================
# 👨‍🎓 STUDENT: VIEW OWN ATTENDANCE
# ======================================================
@login_required
def student_attendance(request):
    """
    Ye view STUDENT ko sirf apni hi attendance dekhne deta hai.
    """

    # ❌ Agar user STUDENT nahi hai to access deny
    if request.user.role != 'STUDENT':
        return render(request, '403.html')

    # ✅ Student sirf apni attendance records dekh sakta hai
    records = Attendance.objects.filter(student=request.user)

    # 📊 Total attendance days
    total_days = records.count()

    # 📊 Present days ('P' = Present)
    present_days = records.filter(status='P').count()

    # 📈 Attendance percentage calculation
    percentage = 0
    if total_days > 0:
        percentage = round((present_days / total_days) * 100, 2)

    return render(request, 'attendance/student_attendance.html', {
        'records': records.order_by('-date'),  # latest attendance upar
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
    Ye view ADMIN aur TEACHER ko monthly attendance report dikhata hai.
    """

    # ❌ Sirf ADMIN ya TEACHER allowed
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return render(request, '403.html')

    # ✅ Sabhi students fetch karo
    students = User.objects.filter(role='STUDENT')

    # URL se month aur year lo (?month=7&year=2025)
    month = request.GET.get('month')
    year = request.GET.get('year')

    # Agar month/year nahi diya gaya to current month/year use karo
    today = date.today()
    month = int(month) if month else today.month
    year = int(year) if year else today.year

    report = []

    # Har student ke liye monthly present / absent count
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
