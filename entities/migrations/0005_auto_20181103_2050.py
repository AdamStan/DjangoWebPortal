# Generated by Django 2.1.2 on 2018-11-03 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0004_plan_fieldofstudy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='subjects',
        ),
        migrations.RemoveField(
            model_name='student',
            name='hoursInWeek',
        ),
        migrations.AddField(
            model_name='scheduledsubject',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Plan'),
        ),
        migrations.AddField(
            model_name='student',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Plan'),
        ),
    ]