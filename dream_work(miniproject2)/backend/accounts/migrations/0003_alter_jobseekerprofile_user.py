# Generated by Django 5.2 on 2025-04-13 12:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_jobseekerprofile_education_jobseekerprofile_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='user',
            field=models.ForeignKey(limit_choices_to={'role': 'job_seeker'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
