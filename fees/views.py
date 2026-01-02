from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

import openpyxl

from .models import StudentFee


# =================================================
# 💰 STUDENT FEES VIEW
# =================================================
@login_required
def student_fees_view(request):
    fees = StudentFee.objects.filter(student=request.user)

    total_amount = sum(
        (fee.fee_structure.amount for fee in fees),
        Decimal('0.00')
    )

    paid_amount = sum(
        (fee.fee_structure.amount for fee in fees if fee.status == 'PAID'),
        Decimal('0.00')
    )

    pending_amount = total_amount - paid_amount

    context = {
        'fees': fees,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
    }

    return render(request, 'student/my_fees.html', context)


# =================================================
# 💳 PAY FEE (DEMO PAYMENT)
# =================================================
@login_required
def pay_fee_view(request, fee_id):
    fee = get_object_or_404(
        StudentFee,
        id=fee_id,
        student=request.user,
        status='PENDING'
    )

    if request.method == "POST":
        fee.status = 'PAID'
        fee.paid_on = timezone.now().date()
        fee.transaction_id = f"TXN{fee.id}{int(timezone.now().timestamp())}"
        fee.save()

    return redirect('student_fees')


# =================================================
# 🧾 PDF FEE RECEIPT
# =================================================
@login_required
def fee_receipt_view(request, fee_id):
    fee = get_object_or_404(
        StudentFee,
        id=fee_id,
        student=request.user,
        status='PAID'
    )

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'inline; filename="fee_receipt_{fee.id}.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 50, "VIDHYA SETU SCHOOL")
    p.setFont("Helvetica", 12)
    p.drawCentredString(width / 2, height - 80, "Fee Payment Receipt")

    y = height - 140
    p.setFont("Helvetica", 11)
    p.drawString(80, y, f"Student Username: {fee.student.username}")
    y -= 25
    p.drawString(80, y, f"Class: {fee.fee_structure.class_name}")
    y -= 25
    p.drawString(80, y, f"Month: {fee.fee_structure.month}")
    y -= 25
    p.drawString(80, y, f"Amount Paid: ₹{fee.fee_structure.amount}")
    y -= 25
    p.drawString(80, y, f"Paid On: {fee.paid_on}")
    y -= 25
    p.drawString(80, y, f"Transaction ID: {fee.transaction_id}")

    p.line(80, y - 30, width - 80, y - 30)
    p.drawString(80, y - 60, "This is a system-generated receipt.")
    p.drawString(80, y - 80, "Thank you for your payment!")

    p.showPage()
    p.save()

    return response


# =================================================
# 📊 ADMIN / TEACHER FEES REPORT
# =================================================
@login_required
def fees_report_view(request):
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("You are not allowed to view this page.")

    fees = StudentFee.objects.select_related(
        'student',
        'student__student_profile',   # ✅ FIXED
        'fee_structure'
    )

    # -------------------------
    # FILTERS
    # -------------------------
    selected_month = request.GET.get('month', '').strip()
    selected_class = request.GET.get('class_name', '').strip()

    if selected_month:
        fees = fees.filter(fee_structure__month=selected_month)

    if selected_class:
        fees = fees.filter(fee_structure__class_name=selected_class)

    # -------------------------
    # TOTALS
    # -------------------------
    total_collected = fees.filter(status='PAID').aggregate(
        total=Sum('fee_structure__amount')
    )['total'] or Decimal('0.00')

    total_pending = fees.filter(status='PENDING').aggregate(
        total=Sum('fee_structure__amount')
    )['total'] or Decimal('0.00')

    # -------------------------
    # CHART DATA
    # -------------------------
    pie_labels = ['Paid', 'Pending']
    pie_values = [float(total_collected), float(total_pending)]

    class_wise = fees.values(
        'fee_structure__class_name'
    ).annotate(
        total=Sum('fee_structure__amount')
    )

    bar_labels = [c['fee_structure__class_name'] for c in class_wise]
    bar_values = [float(c['total']) for c in class_wise]

    months = StudentFee.objects.values_list(
        'fee_structure__month', flat=True
    ).distinct()

    classes = StudentFee.objects.values_list(
        'fee_structure__class_name', flat=True
    ).distinct()

    context = {
        'fees': fees,
        'total_collected': total_collected,
        'total_pending': total_pending,
        'months': months,
        'classes': classes,
        'selected_month': selected_month,
        'selected_class': selected_class,
        'pie_labels': pie_labels,
        'pie_values': pie_values,
        'bar_labels': bar_labels,
        'bar_values': bar_values,
    }

    return render(request, 'fees/fees_report.html', context)


# =================================================
# 📥 EXPORT FEES REPORT TO EXCEL
# =================================================
@login_required
def export_fees_excel(request):
    if request.user.role not in ['ADMIN', 'TEACHER']:
        return HttpResponseForbidden("You are not allowed to export data.")

    fees = StudentFee.objects.select_related(
        'student',
        'student__student_profile',   # ✅ FIXED
        'fee_structure'
    )

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Fees Report"

    ws.append([
        "Student Username",
        "Father Name",
        "Contact Number",
        "Class",
        "Month",
        "Amount",
        "Status"
    ])

    for fee in fees:
        profile = getattr(fee.student, 'student_profile', None)  # ✅ FIXED

        ws.append([
            fee.student.username,
            profile.father_name if profile else "",
            profile.phone if profile else "",
            fee.fee_structure.class_name,
            fee.fee_structure.month,
            float(fee.fee_structure.amount),
            fee.status
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=fees_report.xlsx'
    wb.save(response)

    return response
