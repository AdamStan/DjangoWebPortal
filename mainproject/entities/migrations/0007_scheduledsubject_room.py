# Generated by Django 2.1.2 on 2018-11-05 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0006_auto_20181105_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduledsubject',
            name='room',
            field=models.ForeignKey(default=None, on_delete=True, to='entities.Room'),
        ),
    ]
