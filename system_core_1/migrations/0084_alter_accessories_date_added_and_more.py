# Generated by Django 4.2.7 on 2024-06-03 02:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0083_accountmanager_paid_alter_accessories_date_added_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accessories',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 194198, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 194222, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_approved',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 219950, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_created',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 219901, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accountmanager',
            name='date_updated',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 219932, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalsales',
            name='date_sold',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 195306, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 196431, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 6, 3, 2, 38, 25, 196454, tzinfo=datetime.timezone.utc)),
        ),
    ]
