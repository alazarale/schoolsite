from django.contrib import admin
from .models import Exam, ExamQuestion, ExamGradeAssociation, ExamTaken, Bt


# Register your models here.
class ExamQuestionInLine(admin.StackedInline):
    model = ExamQuestion


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'time', 'created', 'updated']
    inlines = [ExamQuestionInLine]


@admin.register(ExamGradeAssociation)
class ExamGradeAssociationAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']


@admin.register(ExamTaken)
class ExamTakenAdmin(admin.ModelAdmin):
    list_display = ['score', 'wrong']


@admin.register(Bt)
class BtAdmin(admin.ModelAdmin):
    list_display = ['content']