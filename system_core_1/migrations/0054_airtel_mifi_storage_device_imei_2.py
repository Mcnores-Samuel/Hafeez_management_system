# Generated by Django 4.2.7 on 2023-12-28 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0053_specialorders_last_payment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtel_mifi_storage',
            name='device_imei_2',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]
