# Generated by Django 4.2.6 on 2023-12-11 21:20

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('system_core_1', '0042_alter_mainstorage_battery_alter_mainstorage_camera_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='airtel_mifi_storage',
            name='collected_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='mainstorage',
            name='collected_on',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='phone_reference',
            name='cost_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='phone_reference',
            name='current_month',
            field=models.CharField(default='December', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='phone_reference',
            name='final_cash_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='phone_reference',
            name='price_added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='phone_reference',
            name='price_changed_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='mainstorage',
            name='category',
            field=models.CharField(choices=[('Tecno', 'Tecno'), ('Itel', 'Itel'), ('Infinix', 'Infinix'), ('Redmi', 'Redmi'), ('Samsung', 'Samsung'), ('Vivo', 'Vivo'), ('Oppo', 'Oppo'), ('Villaon', 'Villaon')], default='Tecno', max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='mainstorage',
            name='phone_type',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='mainstorage',
            name='screen_size',
            field=models.CharField(blank=True, choices=[('6.8 inch HD+ display', '6.8 inch HD+ display'), ('6.7 inch HD+ display', '6.7 inch HD+ display'), ('6.6 inch HD+ display', '6.6 inch HD+ display'), ('6.5 inch HD+ display', '6.5 inch HD+ display'), ('6.52 inch HD+ display', '6.52 inch HD+ display'), ('6.5 inch HD+ display', '6.5 inch HD+ display'), ('6.52 inch HD+ display', '6.52 inch HD+ display'), ('6.3 inch HD+ display', '6.3 inch HD+ display'), ('5.5 inch HD+ display', '5.5 inch HD+ display'), ('5.45 inch HD+ display', '5.45 inch HD+ display'), ('5.0 inch HD+ display', '5.0 inch HD+ display'), ('4.0 inch HD+ display', '4.0 inch HD+ display'), ('3.5 inch HD+ display', '3.5 inch HD+ display'), ('2.8 inch HD+ display', '2.8 inch HD+ display'), ('2.4 inch HD+ display', '2.4 inch HD+ display'), ('2.0 inch HD+ display', '2.0 inch HD+ display'), ('1.8 inch HD+ display', '1.8 inch HD+ display'), ('1.77 inch display', '1.77 inch display')], max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='mainstorage',
            name='spec',
            field=models.CharField(blank=True, choices=[('8+256', '8+256'), ('4+256', '4+256'), ('8+128', '8+128'), ('4+128', '4+128'), ('4+64', '4+64'), ('3+64', '3+64'), ('2+64', '2+64'), ('3+32', '3+32'), ('2+32', '2+32'), ('1+32', '1+32'), ('2+16', '2+16'), ('1+16', '1+16')], max_length=25, null=True),
        ),
    ]