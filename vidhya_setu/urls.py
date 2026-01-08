from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH / ACCOUNTS
    path('', include('accounts.urls')),

    # DASHBOARD
    path('dashboard/', include('dashboard.urls')),

    # ATTENDANCE
    path('attendance/', include('attendance.urls')),

    # MARKS
    path('marks/', include('marks.urls')),

    # FEES  🔴 (THIS WAS MISSING)
    path('fees/', include('fees.urls')),
]
