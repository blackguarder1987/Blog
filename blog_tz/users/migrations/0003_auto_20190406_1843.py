# Generated by Django 2.1.5 on 2019-04-06 18:43

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20190406_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', upload_to=users.models.save_image_path),
        ),
    ]
