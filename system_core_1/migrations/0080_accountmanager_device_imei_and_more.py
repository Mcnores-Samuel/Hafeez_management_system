# Generated by Django 4.2.7 on 2024-05-16 01:22

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0079_accountmanager_issue_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountmanager',
            name='device_imei',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='accountmanager',
            name='device_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 67811, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 67835, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_created',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 93306, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_updated',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 93337, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalsales',
            name='date_sold',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 68910, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 70084, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 16, 1, 21, 57, 70107, tzinfo=datetime.timezone.utc)),
        ),
    ]