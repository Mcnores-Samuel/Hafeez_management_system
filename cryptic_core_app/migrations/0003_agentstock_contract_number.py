# Generated by Django 4.2.4 on 2023-09-14 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptic_core_app', '0002_remove_customerdata_contract_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentstock',
            name='contract_number',
            field=models.CharField(max_length=8, null=True),
        ),
    ]
