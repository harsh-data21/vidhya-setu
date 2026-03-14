from django.urls import path
from . import views

# Namespace (important for template urls)
app_name = "fees"

urlpatterns = [

    # ================= STUDENT =================
    path("my-fees/", views.my_fees, name="student_fees"),
    path("pay/<int:fee_id>/", views.pay_fee, name="pay_fee"),
    path("receipt/<int:fee_id>/", views.fee_receipt, name="fee_receipt"),

    # ================= ADMIN / TEACHER =================
    path("report/", views.fees_report, name="fees_report"),
    path("export-excel/", views.export_fees_excel, name="export_fees_excel"),
]