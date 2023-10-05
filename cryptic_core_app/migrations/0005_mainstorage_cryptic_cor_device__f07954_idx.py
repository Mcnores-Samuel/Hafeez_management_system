# Generated by Django 4.2.4 on 2023-10-02 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptic_core_app', '0004_agentprofile_contact_number_agentprofile_latitude_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='mainstorage',
            index=models.Index(fields=['device_imei', 'phone_type', 'in_stock', 'assigned'], name='cryptic_cor_device__f07954_idx'),
        ),
    ]
