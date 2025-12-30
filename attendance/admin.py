from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """
    Django Admin configuration for Attendance model
    Ye admin panel me attendance ko easily manage karne ke liye hai
    """

    # ----------------------------------
    # Table me kaun-kaun se columns dikhenge
    # ----------------------------------
    list_display = (
        'student',     # kaunsa student
        'date',        # kis date ki attendance
        'status',      # Present / Absent
        'marked_by',   # kis teacher ne mark ki
        'created_at',  # kab entry bani
    )

    # ----------------------------------
    # Right side filter options
    # ----------------------------------
    list_filter = (
        'status',      # Present / Absent filter
        'date',        # date-wise filter
    )

    # ----------------------------------
    # Search bar configuration
    # ----------------------------------
    search_fields = (
        'student__username',   # student username se search
        'marked_by__username', # teacher username se search
    )

    # ----------------------------------
    # Default ordering (latest first)
    # ----------------------------------
    ordering = ('-date',)

    # ----------------------------------
    # Read-only fields (admin safety)
    # ----------------------------------
    readonly_fields = ('created_at', 'updated_at')

    # ----------------------------------
    # Entries per page
    # ----------------------------------
    list_per_page = 25
