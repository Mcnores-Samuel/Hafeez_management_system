# Generated by Django 4.2.6 on 2023-12-05 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0035_customerdata_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtel_mifi_storage',
            name='secondary_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]