from django.contrib import admin
from .models import Student, Teacher, Parent, StudentParent, TeacherPassword, ParentPassword

# Register your models here.
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['birth_date', 'created', 'updated']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['created', 'user', 'updated']


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['phone', 'created', 'updated']


@admin.register(StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated', 'parent']


@admin.register(TeacherPassword)
class TeacherPasswordAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(ParentPassword)
class ParentPasswordAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']
