from django.db import models
from django.contrib.auth.models import User
from acctype.models import Student, Teacher

# Create your models here.
class AccadamicYear(models.Model):
    STATUS_CHOICE = (('Active', 'Active'),
                     ('Creating', 'Creating'),
                     ('Close', 'Close'))

    name_EC = models.CharField(max_length=4)
    name_GC = models.CharField(max_length=9)
    status = models.CharField(max_length=10, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name_EC


class Grade(models.Model):
    acc_yr = models.ForeignKey(AccadamicYear, related_name='grades', on_delete=models.CASCADE)
    grade_num = models.PositiveIntegerField(blank=True, null=True)
    section = models.CharField(max_length=2, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.grade_num) + self.section
    

class GradeStudent(models.Model):
    grade = models.ForeignKey(Grade, related_name='students', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='grade', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.student.user.username


class Subject(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.name


class GradeSubject(models.Model):
    subject = models.ForeignKey(Subject, related_name='grades', on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, related_name='subjects', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.subject.name


class GrSubTeacher(models.Model):
    gr_sub = models.ForeignKey(GradeSubject, related_name='teacher', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='subjects', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.teacher.user.username


class ExcelStud(models.Model):
    fl = models.FileField(upload_to='stud/excell/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return 'file'


class HomeRoomTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='home_room', on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, related_name="home_room", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.teacher.user.username

