from django.contrib.auth.models import Group
from rest_framework import permissions

def is_in_group(user, group_name):
   
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None

class HasTeacherPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_in_group(request.user, 'teacher')

class HasParentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_in_group(request.user, 'parent')

class HasStudentPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return is_in_group(request.user, 'student')