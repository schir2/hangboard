# Generated by Django 3.0.5 on 2020-05-03 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200503_1710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workout',
            options={'get_latest_by': ('updated',)},
        ),
        migrations.AddField(
            model_name='hold',
            name='position',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='hold',
            unique_together={('position', 'hangboard')},
        ),
        migrations.AlterUniqueTogether(
            name='templateworkoutset',
            unique_together={('position', 'workout')},
        ),
        migrations.AlterUniqueTogether(
            name='workoutset',
            unique_together={('position', 'workout')},
        ),
    ]
