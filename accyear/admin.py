from django.contrib import admin
from .models import AccadamicYear, Grade, GradeStudent, Subject, GradeSubject, GrSubTeacher, ExcelStud, HomeRoomTeacher
# Register your models here.
@admin.register(AccadamicYear)
class AccadamicYearAdmin(admin.ModelAdmin):
    list_display = ['name_EC', 'name_GC', 'created']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['grade_num', 'section','created', 'updated']


@admin.register(GradeStudent)
class GradeStudentAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_diplay = ['name', 'created', 'updated']


@admin.register(GradeSubject)
class GradeSubject(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(GrSubTeacher)
class GrSubTeacherAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(ExcelStud)
class ExcelStudAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(HomeRoomTeacher)
class HomeRoomTeacherAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']
