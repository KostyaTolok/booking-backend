# Generated by Django 4.1.1 on 2022-09-27 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
        ('rooms', '0003_alter_room_images'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RoomImage',
        ),
        migrations.AlterField(
            model_name='room',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='rooms', to='images.image'),
        ),
    ]
