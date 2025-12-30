from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper


def teacher_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'TEACHER':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper


def student_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role == 'STUDENT':
            return view_func(request, *args, **kwargs)
        raise PermissionDenied
    return wrapper
