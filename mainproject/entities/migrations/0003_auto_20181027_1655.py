# Generated by Django 2.1.2 on 2018-10-27 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20181026_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fieldofstudy',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Faculty'),
        ),
        migrations.AlterField(
            model_name='scheduledsubject',
            name='dayOfWeek',
            field=models.CharField(default=None, max_length=32),
        ),
        migrations.AlterField(
            model_name='scheduledsubject',
            name='subject',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Subject'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='fieldOfStudy',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.FieldOfStudy'),
        ),
    ]