# Generated by Django 4.2.6 on 2023-10-26 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0003_userprofile_user_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user_photo',
        ),
    ]
