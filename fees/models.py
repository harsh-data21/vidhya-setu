from django.db import models
from django.conf import settings
from django.utils import timezone


# ==================================================
# 📘 FEE STRUCTURE (CLASS-WISE + MONTHLY)
# ==================================================
class FeeStructure(models.Model):
    """
    Admin defines fee structure
    Class-wise + Month-wise
    """

    CLASS_CHOICES = (
        ('1', 'Class 1'), ('2', 'Class 2'), ('3', 'Class 3'),
        ('4', 'Class 4'), ('5', 'Class 5'), ('6', 'Class 6'),
        ('7', 'Class 7'), ('8', 'Class 8'), ('9', 'Class 9'),
        ('10', 'Class 10'), ('11', 'Class 11'), ('12', 'Class 12'),
    )

    MONTH_CHOICES = (
        ('January', 'January'), ('February', 'February'),
        ('March', 'March'), ('April', 'April'),
        ('May', 'May'), ('June', 'June'),
        ('July', 'July'), ('August', 'August'),
        ('September', 'September'), ('October', 'October'),
        ('November', 'November'), ('December', 'December'),
    )

    class_name = models.CharField(
        max_length=2,
        choices=CLASS_CHOICES
    )

    month = models.CharField(
        max_length=20,
        choices=MONTH_CHOICES
    )

    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Monthly fee amount"
    )

    # 🔥 SQLite-safe (NO auto_now_add)
    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        unique_together = ('class_name', 'month')
        ordering = ('class_name', 'month')
        verbose_name = "Fee Structure"
        verbose_name_plural = "Fee Structures"

    def __str__(self):
        return f"Class {self.class_name} - {self.month} (₹{self.amount})"


# ==================================================
# 💰 STUDENT FEE RECORD
# ==================================================
class StudentFee(models.Model):
    """
    Tracks individual student fee payment
    """

    PAYMENT_STATUS = (
        ('PAID', 'Paid'),
        ('PENDING', 'Pending'),
    )

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'STUDENT'},
        related_name='fees'
    )

    fee_structure = models.ForeignKey(
        FeeStructure,
        on_delete=models.CASCADE,
        related_name='student_fees'
    )

    status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )

    paid_on = models.DateField(
        null=True,
        blank=True
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # 🔥 SQLite-safe (NO auto_now_add)
    created_at = models.DateTimeField(
        default=timezone.now
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Student Fee"
        verbose_name_plural = "Student Fees"

    def __str__(self):
        return f"{self.student.username} - {self.fee_structure.month} ({self.status})"
