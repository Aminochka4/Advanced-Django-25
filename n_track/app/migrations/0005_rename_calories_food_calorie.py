# Generated by Django 5.1.6 on 2025-02-24 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_food_calorie_food_calories_alter_food_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='calories',
            new_name='calorie',
        ),
    ]
