from django.urls import path
from .views import student_fees_view

urlpatterns = [
    path('my-fees/', student_fees_view, name='student_fees'),
]
