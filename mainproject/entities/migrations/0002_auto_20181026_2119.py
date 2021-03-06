# Generated by Django 2.1.2 on 2018-10-26 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181026_2119'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('street', models.CharField(max_length=64)),
                ('city', models.CharField(max_length=32)),
                ('numberOfBuilding', models.CharField(max_length=8)),
                ('postalCode', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('building', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Building')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='student_to_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('yearOfStudy', models.IntegerField(default=None)),
                ('degree', models.IntegerField(default=None)),
                ('hoursInWeek', models.IntegerField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='professor_to_user', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.Faculty')),
            ],
        ),
        migrations.DeleteModel(
            name='Schedule',
        ),
        migrations.RemoveField(
            model_name='scheduledsubject',
            name='hours',
        ),
        migrations.AddField(
            model_name='fieldofstudy',
            name='degree',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='fieldofstudy',
            name='faculty',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Faculty'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduledsubject',
            name='dayOfWeek',
            field=models.CharField(default=None, max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduledsubject',
            name='subject',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.Subject'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduledsubject',
            name='whenFinnish',
            field=models.TimeField(default=None),
        ),
        migrations.AddField(
            model_name='scheduledsubject',
            name='whenStart',
            field=models.TimeField(default=None),
        ),
        migrations.AddField(
            model_name='subject',
            name='fieldOfStudy',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='entities.FieldOfStudy'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='yearOfStudy',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='student',
            name='fieldOfStudy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.FieldOfStudy'),
        ),
        migrations.AddField(
            model_name='plan',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entities.ScheduledSubject'),
        ),
        migrations.AddField(
            model_name='subject',
            name='teachers',
            field=models.ManyToManyField(to='entities.Teacher'),
        ),
    ]
