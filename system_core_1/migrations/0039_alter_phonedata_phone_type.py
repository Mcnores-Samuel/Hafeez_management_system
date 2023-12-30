# Generated by Django 4.2.6 on 2023-12-06 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0038_alter_mainstorage_phone_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonedata',
            name='phone_type',
            field=models.CharField(choices=[('S18', 'S18'), ('A60', 'A60'), ('A04', 'A04'), ('A18', 'A18'), ('C20', 'C20'), ('C19', 'C19'), ('S10Pro', 'S10Pro'), ('S10', 'S10'), ('10C8G', '10C8G'), ('10C', '10C'), ('8C', '8C'), ('P8', 'P8'), ('P7P4G', 'P7P4G'), ('P7P3G', 'P7P3G'), ('P7', 'P7'), ('S9', 'S9'), ('9T', '9T'), ('S8', 'S8'), ('S7', 'S7'), ('it2163', 'it2163'), ('it5607', 'it5607'), ('it5606', 'it5606'), ('it2173', 'it2173'), ('it2171', 'it2171'), ('it2172', 'it2172'), ('13C', '13C'), ('13C Pro', '13C Pro'), ('12C', '12C'), ('12C Pro', '12C Pro'), ('Note 12S', 'Note 12S'), ('Note 12S Pro', 'Note 12S Pro'), ('A2+', 'A2+'), ('A2', 'A2'), ('A1', 'A1'), ('Redmi 10', 'Redmi 10'), ('Redmi 10A', 'Redmi 10A')], default='S18', max_length=25),
        ),
    ]
