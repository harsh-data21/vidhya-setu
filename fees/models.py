from django.db import models
from accounts.models import User

# -------------------------
# Fee Structure (Class-wise / Monthly)
# -------------------------
class FeeStructure(models.Model):
    class_name = models.CharField(max_length=50)
    month = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.class_name} - {self.month}"

# -------------------------
# Student Fee Record
# -------------------------
class StudentFee(models.Model):
    PAYMENT_STATUS = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'}
    )
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='PENDING')
    paid_on = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.fee_structure.month}"
