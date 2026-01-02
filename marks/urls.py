from django.urls import path
from .views import upload_marks, my_marks

urlpatterns = [
    path('teacher/upload-marks/', upload_marks, name='upload_marks'),
    path('student/my-marks/', my_marks, name='my_marks'),
]
