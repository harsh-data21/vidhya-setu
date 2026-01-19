from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """
    Allows access only to authenticated users
    whose role is TEACHER
    """

    message = "Only teachers are allowed to perform this action."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        return getattr(user, 'role', None) == 'TEACHER'
