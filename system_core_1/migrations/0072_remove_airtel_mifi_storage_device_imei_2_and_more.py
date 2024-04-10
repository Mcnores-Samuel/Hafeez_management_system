# Generated by Django 4.2.7 on 2024-03-23 16:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0071_remove_mainstorage_image_mainstorage_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='airtel_mifi_storage',
            name='device_imei_2',
        ),
        migrations.RemoveField(
            model_name='airtel_mifi_storage',
            name='image',
        ),
        migrations.RemoveField(
            model_name='airtel_mifi_storage',
            name='secondary_phone_number',
        ),
        migrations.AddField(
            model_name='airtel_mifi_storage',
            name='cash_recieved_by',
            field=models.CharField(choices=[('Sahil', 'Sahil'), ('Suhail', 'Suhail'), ('Shehzaad', 'Shehzaad'), ("Sahil's Father", "Sahil's Father")], default='Not Paid', max_length=25),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 23, 16, 23, 40, 515851, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 23, 16, 23, 40, 515875, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalsales',
            name='date_sold',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 23, 16, 23, 40, 517475, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 23, 16, 23, 40, 519304, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 3, 23, 16, 23, 40, 519331, tzinfo=datetime.timezone.utc)),
        ),
    ]