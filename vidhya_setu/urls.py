from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # ----------------------------
    # Admin
    # ----------------------------
    path('admin/', admin.site.urls),

    # ----------------------------
    # Auth / Accounts
    # ----------------------------
    path('', include('accounts.urls')),

    # ----------------------------
    # Dashboard
    # ----------------------------
    path('dashboard/', include('dashboard.urls')),

    # ----------------------------
    # Attendance
    # ----------------------------
    path('attendance/', include('attendance.urls')),

    # ----------------------------
    # Marks
    # ----------------------------
    path('marks/', include('marks.urls')),

    # ----------------------------
    # Fees
    # ----------------------------
    path('fees/', include('fees.urls')),
]
