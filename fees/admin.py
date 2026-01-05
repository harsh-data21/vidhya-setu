from django.contrib import admin
from .models import FeeStructure, StudentFee


# ==================================================
# 📘 FEE STRUCTURE ADMIN
# ==================================================
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    """
    Admin configuration for class-wise & month-wise fee structure
    """

    list_display = (
        'class_name',
        'month',
        'amount',
        'created_at',
    )

    list_filter = (
        'class_name',
        'month',
    )

    search_fields = (
        'class_name',
        'month',
    )

    ordering = (
        'class_name',
        'month',
    )

    list_per_page = 25


# ==================================================
# 💰 STUDENT FEE ADMIN
# ==================================================
@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    """
    Admin configuration for student fee records
    """

    list_display = (
        'student',
        'get_class',
        'get_month',
        'get_amount',
        'status',
        'paid_on',
        'transaction_id',
    )

    list_filter = (
        'status',
        'fee_structure__class_name',
        'fee_structure__month',
    )

    search_fields = (
        'student__username',
        'transaction_id',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    # -------- Helper methods --------
    def get_class(self, obj):
        return obj.fee_structure.class_name
    get_class.short_description = "Class"

    def get_month(self, obj):
        return obj.fee_structure.month
    get_month.short_description = "Month"

    def get_amount(self, obj):
        return obj.fee_structure.amount
    get_amount.short_description = "Amount"
