from django.db import models
from django.contrib.auth.models import User
from course.models import Module
from accyear.models import Subject, Grade
from ckeditor.fields import RichTextField


# Create your models here.
# class ExamRound(models.Model):
#     STAT_CHOICE = (('Hide', 'Hide'),
#                    ('Show', 'Show'))

#     name = models.CharField(max_length=50)
#     show_result = models.DateTimeField()
#     status = models.CharField(max_length=5, choices=STAT_CHOICE, default='Hide')
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['-created']
    
#     def __str__(self):
#         return self.name
    


class Exam(models.Model):
    choice = (('draft', 'Draft'),
              ('active', 'Active'))
    owner = models.ForeignKey(User, related_name='exams', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='exams', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    time = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=choice, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


class ExamGradeAssociation(models.Model):
    grade = models.ForeignKey(Grade, related_name='exam_association', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name='grade_association', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return str(self.grade.grade_num) + self.grade.section
    


class ExamQuestion(models.Model):
    choice = (('choice_a', 'Choice A'),
              ('choice_b', 'Choice B'),
              ('choice_c', 'Choice C'),
              ('choice_d', 'Choice D'))
    exam = models.ForeignKey(Exam, related_name='exam_questions', on_delete=models.CASCADE)
    module = models.ForeignKey(Module, related_name='exam_questions', on_delete=models.CASCADE, blank=True, null=True)
    question = models.TextField()
    choice_a = models.CharField(max_length=300)
    choice_b = models.CharField(max_length=300)
    choice_c = models.CharField(max_length=300)
    choice_d = models.CharField(max_length=300)
    answer = models.CharField(max_length=10, choices=choice)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.question[:10]


class ExamTaken(models.Model):
    exam = models.ForeignKey(Exam, related_name='taken', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='exam_taken', on_delete=models.CASCADE)
    score = models.IntegerField()
    wrong = models.CharField(max_length=1000, null=True, blank=True)
    unanswered = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.wrong


class Bt(models.Model):
    content = RichTextField()




