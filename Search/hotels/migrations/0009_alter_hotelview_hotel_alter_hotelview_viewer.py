# Generated by Django 4.1.2 on 2022-10-15 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0008_hotelview_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelview',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='views', to='hotels.hotel'),
        ),
        migrations.AlterField(
            model_name='hotelview',
            name='viewer',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]