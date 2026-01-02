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
        'student',          # Kaunsa student
        'date',             # Kis date ki attendance
        'status_display',   # Present / Absent (human readable)
        'marked_by',        # Kis teacher ne mark ki
        'created_at',       # Kab record create hua
    )

    # ==================================================
    # 🎯 Right sidebar filters
    # ==================================================
    list_filter = (
        'status',           # Present / Absent
        'date',             # Date-wise
        'marked_by',        # Teacher-wise
    )

    # ==================================================
    # 🔍 Search box configuration
    # ==================================================
    search_fields = (
        'student__username',
        'marked_by__username',
    )

    # ==================================================
    # ⚡ Query optimization
    # ==================================================
    list_select_related = ('student', 'marked_by')

    # ==================================================
    # ⬇️ Default ordering (latest attendance upar)
    # ==================================================
    ordering = ('-date', 'student')

    # ==================================================
    # 🔒 Read-only fields (data safety)
    # ==================================================
    readonly_fields = (
        'created_at',
        'updated_at',
    )

    # ==================================================
    # 📄 Pagination
    # ==================================================
    list_per_page = 25

    # ==================================================
    # 📅 Date hierarchy (top navigation)
    # ==================================================
    date_hierarchy = 'date'

    # ==================================================
    # 🎨 Custom display helpers
    # ==================================================
    def status_display(self, obj):
        return obj.get_status_display()
    status_display.short_description = 'Status'
