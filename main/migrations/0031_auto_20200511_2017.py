# Generated by Django 3.0.5 on 2020-05-12 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0030_auto_20200511_2014'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='templateworkoutset',
            unique_together={('previous', 'workout')},
        ),
        migrations.AlterUniqueTogether(
            name='workoutset',
            unique_together={('previous', 'workout')},
        ),
    ]