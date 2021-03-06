# Generated by Django 2.1.2 on 2018-11-05 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_auto_20181103_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='faculty',
            name='description',
            field=models.CharField(default=None, max_length=256),
        ),
        migrations.AlterField(
            model_name='fieldofstudy',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.Faculty'),
        ),
        migrations.AlterField(
            model_name='plan',
            name='fieldOfStudy',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.FieldOfStudy'),
        ),
        migrations.AlterField(
            model_name='room',
            name='building',
            field=models.ForeignKey(on_delete=True, to='entities.Building'),
        ),
        migrations.AlterField(
            model_name='scheduledsubject',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.Plan'),
        ),
        migrations.AlterField(
            model_name='scheduledsubject',
            name='subject',
            field=models.OneToOneField(default=None, on_delete=True, to='entities.Subject'),
        ),
        migrations.AlterField(
            model_name='student',
            name='fieldOfStudy',
            field=models.ForeignKey(on_delete=True, to='entities.FieldOfStudy'),
        ),
        migrations.AlterField(
            model_name='student',
            name='plan',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.Plan'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='fieldOfStudy',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.FieldOfStudy'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='faculty',
            field=models.ForeignKey(on_delete=True, to='entities.Faculty'),
        ),
    ]
