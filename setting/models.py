from django.db import models


# Create your models here.
class GradeExcel(models.Model):
    file = models.FileField(upload_to='grade/excel/')


class StudentUserInfo(models.Model):
    user_id = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=20, blank=True, null=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
