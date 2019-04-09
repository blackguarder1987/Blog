# Generated by Django 2.1.5 on 2019-04-09 17:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20190409_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislikes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='comments',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 9, 17, 14, 14, 715611)),
        ),
    ]
