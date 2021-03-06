# Generated by Django 2.1.5 on 2019-04-06 13:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to=users.models.save_image_path),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
