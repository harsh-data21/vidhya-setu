from django.contrib import admin
from .models import FeeStructure, StudentFee

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'month', 'amount')
    list_filter = ('class_name', 'month')

@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_structure', 'status', 'paid_on')
    list_filter = ('status',)
