# Generated by Django 2.1.2 on 2018-10-27 14:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20181026_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='whenCreated',
            field=models.DateField(default=datetime.date.today),
        ),
    ]