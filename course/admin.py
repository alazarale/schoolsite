from django.contrib import admin
from .models import Course, Module, CourseGradeAssociation


# Register your models here.

class ModuleInLine(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'subject', 'created']
    list_filter = ['created', 'subject']
    search_fields = ['title', 'overview']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ModuleInLine]


@admin.register(CourseGradeAssociation)
class CourseGradeAssociationAdmin(admin.ModelAdmin):
    list_display = ['grades', 'course']
