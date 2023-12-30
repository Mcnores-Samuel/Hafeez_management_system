# Generated by Django 4.2.6 on 2023-11-07 01:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0014_alter_customerdata_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerdata',
            name='working_status',
        ),
        migrations.AddField(
            model_name='customerdata',
            name='account_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerdata',
            name='employer_or_coleague',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='customerdata',
            name='employer_or_coleague_contact',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
        migrations.AddField(
            model_name='customerdata',
            name='workplace',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='created_at',
            field=models.DateField(default=datetime.datetime(2023, 11, 7, 1, 3, 52, 532469, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='customerdata',
            name='update_at',
            field=models.DateField(default=datetime.datetime(2023, 11, 7, 1, 3, 52, 532513, tzinfo=datetime.timezone.utc)),
        ),
    ]