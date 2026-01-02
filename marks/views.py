from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from accounts.models import User, StudentProfile
from .models import Subject, StudentMark


# ==================================================
# 📝 TEACHER: UPLOAD MARKS (CLASS → SECTION → ROLL WISE)
# ==================================================
@login_required
def upload_marks(request):
    """
    📝 Upload Marks View (Teacher Only)
    ----------------------------------
    - Sirf TEACHER role access kar sakta hai
    - Teacher ki assigned class & section ke students hi dikhenge
    - Students roll number wise ordered honge
    - Teacher decide karega exam kitne marks ka hai
    """

    # -----------------------------
    # 🔐 ROLE CHECK
    # -----------------------------
    if request.user.role != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    # -----------------------------
    # 👨‍🏫 Teacher Profile
    # -----------------------------
    teacher_profile = request.user.teacher_profile
    assigned_class = teacher_profile.assigned_class
    assigned_section = teacher_profile.assigned_section

    # -----------------------------
    # 🎓 STUDENTS (Class + Section + Roll wise)
    # -----------------------------
    student_profiles = StudentProfile.objects.filter(
        student_class=assigned_class,
        section=assigned_section
    ).select_related('user').order_by('roll_no')

    students = [sp.user for sp in student_profiles]

    subjects = Subject.objects.all().order_by('name')

    # -----------------------------
    # 📝 FORM SUBMIT (POST)
    # -----------------------------
    if request.method == 'POST':

        subject_id = request.POST.get('subject')
        max_marks = request.POST.get('max_marks')

        if not subject_id or not max_marks:
            messages.error(request, "Subject and total marks are required ❌")
            return redirect('upload_marks')

        if not max_marks.isdigit() or int(max_marks) <= 0:
            messages.error(request, "Total marks must be a positive number ❌")
            return redirect('upload_marks')

        subject = get_object_or_404(Subject, id=subject_id)
        max_marks = int(max_marks)

        saved_count = 0

        # -----------------------------
        # 🔁 Save marks roll-wise
        # -----------------------------
        for sp in student_profiles:
            student = sp.user
            marks = request.POST.get(f"marks_{student.id}")

            if not marks or not marks.isdigit():
                continue

            marks = int(marks)

            if marks < 0 or marks > max_marks:
                continue

            StudentMark.objects.update_or_create(
                student=student,
                subject=subject,
                defaults={
                    'marks_obtained': marks,
                    'max_marks': max_marks,
                    'uploaded_by': request.user
                }
            )

            saved_count += 1

        # -----------------------------
        # ✅ Messages
        # -----------------------------
        if saved_count == 0:
            messages.warning(
                request,
                "No marks were saved. Please enter valid marks ⚠️"
            )
        else:
            messages.success(
                request,
                f"Marks uploaded successfully ✅ ({saved_count} students)"
            )

        return redirect('upload_marks')

    # -----------------------------
    # 📄 PAGE LOAD (GET)
    # -----------------------------
    return render(
        request,
        'marks/upload_marks.html',
        {
            'students': students,
            'subjects': subjects,
            'class_name': assigned_class,
            'section': assigned_section,
        }
    )


# ==================================================
# 📊 STUDENT: VIEW MY MARKS
# ==================================================
@login_required
def my_marks(request):
    """
    📊 Student apne hi marks dekhe
    """

    if request.user.role != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    marks = StudentMark.objects.filter(
        student=request.user
    ).select_related('subject').order_by('subject__name')

    return render(request, 'marks/my_marks.html', {
        'marks': marks
    })
