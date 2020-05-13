# Generated by Django 3.0.5 on 2020-05-13 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_auto_20200512_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateworkoutset',
            name='previous',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='previous_workoutset', to='main.TemplateWorkoutSet'),
        ),
        migrations.AlterField(
            model_name='workoutset',
            name='previous',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='previous_workoutset', to='main.WorkoutSet'),
        ),
    ]
