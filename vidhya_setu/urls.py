from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    # ----------------------------
    # Django Admin
    # ----------------------------
    path('admin/', admin.site.urls),

    # ----------------------------
    # Accounts / Authentication
    # ----------------------------
    path('', include('accounts.urls')),

    # ----------------------------
    # Dashboard (Admin/Teacher/Student)
    # ----------------------------
    path('dashboard/', include('dashboard.urls')),

    # ----------------------------
    # Attendance Module
    # ----------------------------
    path('attendance/', include('attendance.urls')),

    # ----------------------------
    # Marks Module
    # ----------------------------
    path('marks/', include('marks.urls')),

    # ----------------------------
    # Fees Module
    # ----------------------------
    path('fees/', include('fees.urls')),
]