# Generated by Django 4.2.7 on 2024-01-02 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0055_mainstorage_device_imei_2_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonedata',
            name='phone_type',
            field=models.CharField(default='N/A', max_length=25),
        ),
    ]
