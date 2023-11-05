# Generated by Django 3.0.6 on 2022-06-29 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0003_auto_20220629_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='desc_file',
            field=models.FileField(blank=True, null=True, upload_to='teacher/assignment/file'),
        ),
        migrations.AddField(
            model_name='homework',
            name='desc_file',
            field=models.FileField(blank=True, null=True, upload_to='teacher/homework/file'),
        ),
    ]
