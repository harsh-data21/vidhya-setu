from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

from accounts.models import StudentProfile
from .models import Subject, StudentMark


# ==================================================
# 📝 TEACHER: UPLOAD MARKS (CLASS → SECTION → ROLL WISE)
# ==================================================
@login_required
def upload_marks(request):
    """
    Upload Marks View (Teacher Only)

    - Sirf TEACHER access
    - Assigned class & section ke students
    - Roll number wise entry
    """

    # -----------------------------
    # 🔐 ROLE CHECK
    # -----------------------------
    if getattr(request.user, 'role', None) != 'TEACHER':
        return HttpResponseForbidden("Access Denied")

    # -----------------------------
    # 👨‍🏫 Teacher Profile
    # -----------------------------
    try:
        teacher_profile = request.user.teacher_profile
    except AttributeError:
        messages.error(request, "Teacher profile not found ❌")
        return redirect('teacher_dashboard')

    assigned_class = teacher_profile.assigned_class
    assigned_section = teacher_profile.assigned_section

    # -----------------------------
    # 🎓 STUDENTS (Class + Section)
    # -----------------------------
    student_profiles = (
        StudentProfile.objects
        .filter(
            student_class=assigned_class,
            section=assigned_section
        )
        .select_related('user')
        .order_by('roll_no')
    )

    # -----------------------------
    # 📚 SUBJECTS (Only this class)
    # -----------------------------
    subjects = Subject.objects.filter(
        class_name=assigned_class
    ).order_by('name')

    # -----------------------------
    # 📝 FORM SUBMIT
    # -----------------------------
    if request.method == 'POST':

        subject_id = request.POST.get('subject')
        exam_name = request.POST.get('exam_name', 'Unit Test').strip()
        total_marks = request.POST.get('total_marks')

        # -----------------------------
        # ❌ BASIC VALIDATION
        # -----------------------------
        if not subject_id or not total_marks:
            messages.error(request, "Subject and total marks are required ❌")
            return redirect('marks:upload_marks')

        if not total_marks.isdigit() or int(total_marks) <= 0:
            messages.error(request, "Total marks must be a positive number ❌")
            return redirect('marks:upload_marks')

        subject = get_object_or_404(
            Subject,
            id=subject_id,
            class_name=assigned_class
        )

        total_marks = int(total_marks)
        saved_count = 0

        # -----------------------------
        # 🔁 SAVE MARKS (ROLL WISE)
        # -----------------------------
        for sp in student_profiles:
            student = sp.user
            marks_value = request.POST.get(f"marks_{student.id}")

            if not marks_value or not marks_value.isdigit():
                continue

            marks_value = int(marks_value)

            if marks_value < 0 or marks_value > total_marks:
                continue

            StudentMark.objects.update_or_create(
                student=student,
                subject=subject,
                exam_name=exam_name,
                defaults={
                    'marks_obtained': marks_value,
                    'total_marks': total_marks,
                    'uploaded_by': request.user
                }
            )

            saved_count += 1

        # -----------------------------
        # ✅ FEEDBACK
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

        return redirect('marks:upload_marks')

    # -----------------------------
    # 📄 PAGE LOAD (GET)
    # -----------------------------
    return render(
        request,
        'marks/upload_marks.html',
        {
            'students': student_profiles,
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
    Student apne hi marks dekhe
    + Exam-wise filter
    """

    if getattr(request.user, 'role', None) != 'STUDENT':
        return HttpResponseForbidden("Access Denied")

    selected_exam = request.GET.get('exam')

    marks_qs = (
        StudentMark.objects
        .filter(student=request.user)
        .select_related('subject')
    )

    if selected_exam:
        marks_qs = marks_qs.filter(exam_name=selected_exam)

    marks_qs = marks_qs.order_by('subject__name')

    # Dropdown ke liye exam list
    exams = (
        StudentMark.objects
        .filter(student=request.user)
        .values_list('exam_name', flat=True)
        .distinct()
    )

    return render(
        request,
        'marks/my_marks.html',
        {
            'marks': marks_qs,
            'exams': exams,
            'selected_exam': selected_exam
        }
    )
