# Generated by Django 4.2.6 on 2023-12-02 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0031_airtel_mifi_storage_comment_mainstorage_comment_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainstorage',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]