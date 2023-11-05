from statistics import mode
import django
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    GENDER_CHOICE = (('Male', 'Male'),
                     ('Female', 'Female'))

    user = models.ForeignKey(User, related_name='student', on_delete=models.CASCADE)
    stud_id = models.CharField(max_length=50, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="student/profile_pic/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.user.username


class Parent(models.Model):
    RELATION_CHOICE = (('Mother', 'Mother'),
                     ('Father', 'Father'),
                     ('Other', 'Other'))
    
    user = models.ForeignKey(User, related_name='parent', on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, blank=True, null=True)
    job = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    relation_ship = models.CharField(max_length=20, choices=RELATION_CHOICE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    STATUS_CHOICE = (('Active', 'Active'),
                     ('Deactivated', 'Deactivated'))

    user = models.ForeignKey(User, null=True, blank=True, related_name='teacher', on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=10)
    birth_date = models.DateField(blank=True, null=True)
    hired_date = models.DateField()
    profile_pic = models.ImageField(upload_to="teacher/profile", blank=True, null=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.phone


class StudentParent(models.Model):
    student = models.ForeignKey(Student, related_name='parent', on_delete=models.CASCADE)
    parent = models.ForeignKey(Parent, related_name='students', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.parent.user.username


class TeacherPassword(models.Model):
    teacher = models.ForeignKey(Teacher, related_name='pass_w', on_delete=models.CASCADE)
    pass_w = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.teacher.phone


class ParentPassword(models.Model):
    parent = models.ForeignKey(Parent, related_name='pass_w', on_delete=models.CASCADE)
    pass_w = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return self.parent.phone
    
        




