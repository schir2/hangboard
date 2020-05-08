# Generated by Django 3.0.5 on 2020-05-08 21:35

from django.db import migrations, models
import main.managers


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0021_auto_20200507_1942'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='templateworkout',
            managers=[
                ('objects', main.managers.WorkoutManager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='workout',
            managers=[
                ('objects', main.managers.WorkoutManager()),
            ],
        ),
        migrations.AlterField(
            model_name='templateworkout',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
