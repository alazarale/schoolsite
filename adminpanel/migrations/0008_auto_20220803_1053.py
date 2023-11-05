# Generated by Django 3.0.6 on 2022-08-03 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accyear', '0001_initial'),
        ('adminpanel', '0007_classschedule_rest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classschedule',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='accyear.Subject'),
        ),
    ]