# Generated by Django 3.0.5 on 2020-05-11 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20200511_1658'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templateworkoutset',
            name='custom',
        ),
        migrations.RemoveField(
            model_name='templateworkoutset',
            name='position',
        ),
        migrations.RemoveField(
            model_name='workoutset',
            name='custom',
        ),
        migrations.RemoveField(
            model_name='workoutset',
            name='position',
        ),
    ]
