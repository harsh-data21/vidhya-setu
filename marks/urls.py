from django.urls import path
from .views import upload_marks, my_marks

app_name = 'marks'   # ✅ Namespacing (BEST PRACTICE)

urlpatterns = [
    # 📝 TEACHER: Upload marks (HTML view)
    path(
        'teacher/upload-marks/',
        upload_marks,
        name='upload_marks'
    ),

    # 📊 STUDENT: View own marks (HTML view)
    path(
        'student/my-marks/',
        my_marks,
        name='my_marks'
    ),
]
