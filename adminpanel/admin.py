from django.contrib import admin
from .models import Result, StudentResult, Attendance, FinalScore, PreviousGrade, Homework, Assignment, ScheduleTimes, ClassSchedule, SchoolPayment, SPGradeAssociation, SPPaid


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['description', 'out_of']

@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):
    list_display = ['score', 'created']

@admin.register(Attendance)
class AttendaceAdmin(admin.ModelAdmin):
    list_display = ['att_date', 'updated']

@admin.register(FinalScore)
class FinalScoreAdmin(admin.ModelAdmin):
    list_display = ['created', 'updated']

@admin.register(PreviousGrade)
class PreviousGradeAdmin(admin.ModelAdmin):
    list_display = ['score', 'created', 'updated']

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'for_who', 'due_date']

@admin.register(Assignment)
class AssigmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'kind', 'due_date']

@admin.register(ScheduleTimes)
class ScheduleTimesAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'created']

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['sc_day', 'created', 'updated']

@admin.register(SchoolPayment)
class SchoolPaymentAdmin(admin.ModelAdmin):
    list_display = ['title', 'payment_starts', 'payment_ends']

@admin.register(SPGradeAssociation)
class SPGradeAssociationAdmin(admin.ModelAdmin):
    list_display = ['amount', 'created', 'updated']

@admin.register(SPPaid)
class SPPaidAdmin(admin.ModelAdmin):
    list_display = ['paid_on', 'sp']
