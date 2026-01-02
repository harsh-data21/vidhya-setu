from django.urls import path
from .views import (
    student_fees_view,
    pay_fee_view,
    fee_receipt_view,
    fees_report_view,
    export_fees_excel,
)

urlpatterns = [
    path('my-fees/', student_fees_view, name='student_fees'),
    path('pay/<int:fee_id>/', pay_fee_view, name='pay_fee'),
    path('receipt/<int:fee_id>/', fee_receipt_view, name='fee_receipt'),

    # 📊 Admin / Teacher
    path('report/', fees_report_view, name='fees_report'),
    path('export-excel/', export_fees_excel, name='export_fees_excel'),

]
