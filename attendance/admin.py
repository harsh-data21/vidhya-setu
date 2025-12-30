from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Attendance model

    Is class ka use admin panel me attendance records
    ko easily dekhne, filter karne aur search karne ke liye hota hai.
    """

    # ==================================================
    # 📋 Admin list page par dikhne wale columns
    # ==================================================
    list_display = (
        'student',      # Kaunsa student
        'date',         # Kis date ki attendance
        'status',       # P / A (Present / Absent)
        'marked_by',    # Kis teacher ne mark ki
        'created_at',   # Kab record create hua
    )

    # ==================================================
    # 🎯 Right sidebar filters
    # ==================================================
    list_filter = (
        'status',       # Present / Absent filter
        'date',         # Date-wise filter
    )

    # ==================================================
    # 🔍 Search box configuration
    # ==================================================
    search_fields = (
        'student__username',    # Student username se search
        'marked_by__username',  # Teacher username se search
    )

    # ==================================================
    # ⬇️ Default ordering (latest attendance upar)
    # ==================================================
    ordering = ('-date',)

    # ==================================================
    # 🔒 Read-only fields (data safety ke liye)
    # ==================================================
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    # ==================================================
    # 📄 Pagination (ek page par records)
    # ==================================================
    list_per_page = 25
