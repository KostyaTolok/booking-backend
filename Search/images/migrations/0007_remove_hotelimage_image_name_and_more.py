# Generated by Django 4.1.1 on 2022-10-04 21:49

import images.utils
from django.db import migrations, models
import functools


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0006_alter_hotelimage_image_key'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelimage',
            name='image_name',
        ),
        migrations.AlterField(
            model_name='hotelimage',
            name='image_key',
            field=models.ImageField(upload_to=functools.partial(images.utils.path_and_rename, *(), **{'path': 'hotels'}), verbose_name='Image key'),
        ),
        migrations.AlterField(
            model_name='roomimage',
            name='image_key',
            field=models.ImageField(upload_to=functools.partial(images.utils.path_and_rename, *(), **{'path': 'rooms'}), verbose_name='Image key'),
        ),
    ]
