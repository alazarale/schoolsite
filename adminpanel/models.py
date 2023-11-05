from pyexpat import model
from django.db import models
from accyear.models import Grade, GradeSubject, GradeStudent, Subject 
from acctype.models import Student


class Result(models.Model):
    PRIVACY_CHOICE = (('Student', 'Student'),
                     ('All', 'All'))

    gr_sub = models.ForeignKey(GradeSubject, related_name='results', on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    out_of = models.FloatField()
    privacy = models.CharField(max_length=10, choices=PRIVACY_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.description


class StudentResult(models.Model):
    result = models.ForeignKey(Result, related_name='result', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='result', on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.result.description
    

class Attendance(models.Model):
    ATT_CHOICE = (('Present', 'P'),
                 ('Absent', 'A'),
                 ('Leave', 'L'),
                 ('Close', 'Close'))

    student = models.ForeignKey(Student, related_name='attendaces', on_delete=models.CASCADE)
    stat = models.CharField(max_length=10, choices=ATT_CHOICE)
    att_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-att_date']
    
    def __str__(self):
        return self.student.user.username


class FinalScore(models.Model):
    gr_stud = models.ForeignKey(GradeStudent, related_name="final_score", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="final_score", on_delete=models.CASCADE)
    first_desc = models.TextField(blank=True, null=True)
    first_50 = models.FloatField(blank=True, null=True)
    second_desc = models.TextField(blank=True, null=True)
    second_50 = models.FloatField(blank=True, null=True)
    third_desc = models.TextField(blank=True, null=True)
    third_50 = models.FloatField(blank=True, null=True)
    forth_desc = models.TextField(blank=True, null=True)
    forth_50 = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.subject.name


class PreviousGrade(models.Model):
    student = models.ForeignKey(Student, related_name="previous_score", on_delete=models.CASCADE)
    score = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.student.stud_id


class Homework(models.Model):
    forwhoChoice = (('All Class', 'All Class'),
                 ('Student', 'Student'),)

    gr_sub = models.ForeignKey(GradeSubject, related_name='homeworks', blank=True, null=True, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='homework', blank=True, null=True, on_delete=models.CASCADE)
    for_who = models.CharField(max_length=10, choices=forwhoChoice)
    title = models.CharField(max_length=100)
    description = models.TextField()
    desc_file = models.FileField(upload_to='teacher/homework/file', blank=True, null=True)
    due_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title


class Assignment(models.Model):
    forwhoChoice = (('Group', 'Group'),
                 ('Individual', 'Individual'),)
    yesNo = (('Yes', 'Yes'),
                 ('No', 'No'),)
    
    gr_sub = models.ForeignKey(GradeSubject, related_name='assignments', on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=forwhoChoice)
    amount = models.PositiveIntegerField(blank=True, null=True)
    title = models.CharField(max_length=100)
    chapters = models.CharField(max_length=200)
    description = models.TextField()
    desc_file = models.FileField(upload_to='teacher/assignment/file', blank=True, null=True)
    graded = models.CharField(max_length=5, choices=yesNo)
    out_of = models.PositiveIntegerField(blank=True, null=True)
    due_date = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.title


class ScheduleTimes(models.Model):
    start = models.TimeField()
    end = models.TimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start']
    
    def __str__(self):
        return str(self.start)


class ClassSchedule(models.Model):
    DAY_CHOICE = (('Monday', 'Monday'),
                 ('Tuesday', 'Tuesday'),
                 ('Wednesday', 'Wednesday'),
                 ('Thursday', 'Thursday'),
                 ('Friday', 'Friday'),)


    grade = models.ForeignKey(Grade, related_name='schedules', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="schedules", blank=True, null=True, on_delete=models.CASCADE)
    schedule_time = models.ForeignKey(ScheduleTimes, related_name='class_schedule', on_delete=models.CASCADE)
    sc_day = models.CharField(max_length=10, choices=DAY_CHOICE)
    rest = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['schedule_time']
    
    def __str__(self):
        return self.sc_day
    

class SchoolPayment(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    payment_starts = models.DateField()
    payment_ends = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['payment_starts']
    
    def __str__(self):
        return self.title


class SPGradeAssociation(models.Model):
    sp = models.ForeignKey(SchoolPayment, related_name='grade', on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, related_name='school_payment', on_delete=models.CASCADE)
    amount = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sp']
    
    def __str__(self):
        return 'associated'


class SPPaid(models.Model):
    sp = models.ForeignKey(SchoolPayment, related_name='paid', on_delete=models.CASCADE)
    stud = models.ForeignKey(Student, related_name='paid', on_delete=models.CASCADE)
    paid_on = models.DateField()

    class Meta:
        ordering = ['-paid_on']
    
    def __str__(self):
        return 'done'



