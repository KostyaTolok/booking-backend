# Generated by Django 4.1.2 on 2022-10-12 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_hotelviews'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HotelViews',
            new_name='HotelView',
        ),
    ]
