# Generated by Django 3.0.5 on 2020-05-03 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200502_2305'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='hangboard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Hangboard'),
            preserve_default=False,
        ),
    ]