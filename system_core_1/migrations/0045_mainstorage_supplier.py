# Generated by Django 4.2.6 on 2023-12-15 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0044_mainstorage_on_display'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainstorage',
            name='supplier',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
