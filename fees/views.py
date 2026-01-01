from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import StudentFee

@login_required
def student_fees_view(request):
    # sirf logged-in student ki fees
    fees = StudentFee.objects.filter(student=request.user)

    total_amount = sum(f.fee_structure.amount for f in fees)
    paid_amount = sum(
        f.fee_structure.amount for f in fees if f.status == 'PAID'
    )
    pending_amount = total_amount - paid_amount

    context = {
        'fees': fees,
        'total_amount': total_amount,
        'paid_amount': paid_amount,
        'pending_amount': pending_amount,
    }

    return render(request, 'student/my_fees.html', context)
