# Generated by Django 4.2.7 on 2024-06-03 02:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0082_accountmanager_date_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmanager',
            name='paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 36, 37, 508773, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 36, 37, 508796, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_approved',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 3, 2, 36, 37, 534142, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 3, 2, 36, 37, 534089, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_updated',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 3, 2, 36, 37, 534121, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalsales',
            name='date_sold',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 36, 37, 509920, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 36, 37, 511073, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 36, 37, 511096, tzinfo=datetime.timezone.utc)),
        ),
    ]
