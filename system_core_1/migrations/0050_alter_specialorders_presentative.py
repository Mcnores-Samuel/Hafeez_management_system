# Generated by Django 4.2.6 on 2023-12-19 22:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0049_alter_specialorders_presentative'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialorders',
            name='presentative',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
