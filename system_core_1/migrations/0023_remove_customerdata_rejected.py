# Generated by Django 4.2.6 on 2023-11-09 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0022_customerdata_approved_customerdata_pending_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerdata',
            name='rejected',
        ),
    ]
