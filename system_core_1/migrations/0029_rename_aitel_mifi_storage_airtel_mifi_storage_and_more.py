# Generated by Django 4.2.6 on 2023-11-15 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0028_aitel_mifi_storage_phone_number'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Aitel_mifi_storage',
            new_name='Airtel_mifi_storage',
        ),
        migrations.RenameIndex(
            model_name='airtel_mifi_storage',
            new_name='system_core_device__19a356_idx',
            old_name='system_core_device__d21b0e_idx',
        ),
    ]