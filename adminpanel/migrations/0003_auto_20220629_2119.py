# Generated by Django 3.0.6 on 2022-06-29 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0002_assignment_homework'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homework',
            old_name='dscription',
            new_name='description',
        ),
    ]
