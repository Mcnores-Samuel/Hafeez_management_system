# Generated by Django 4.2.7 on 2024-02-12 23:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0067_refarbisheddevices_finalsales_accessories'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialorders',
            name='current_payment',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 2, 12, 23, 5, 8, 477322, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='accessories',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 2, 12, 23, 5, 8, 477346, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='finalsales',
            name='date_sold',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 2, 12, 23, 5, 8, 478447, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_added',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 2, 12, 23, 5, 8, 479572, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='refarbisheddevices',
            name='date_modified',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 2, 12, 23, 5, 8, 479596, tzinfo=datetime.timezone.utc)),
        ),
    ]