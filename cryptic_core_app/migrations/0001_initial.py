# Generated by Django 4.2.4 on 2023-09-08 15:13

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0014_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_agent', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(null=True)),
                ('update_at', models.DateTimeField()),
                ('customer_name', models.CharField(max_length=50)),
                ('national_id', models.CharField(max_length=9)),
                ('customer_contact', models.CharField(max_length=13)),
                ('second_contact', models.CharField(max_length=13, null=True)),
                ('first_witness_name', models.CharField(max_length=50)),
                ('first_witness_contact', models.CharField(max_length=13)),
                ('second_witness_name', models.CharField(max_length=50)),
                ('second_witness_contact', models.CharField(max_length=13)),
                ('customer_location', models.CharField(max_length=50)),
                ('nearest_school', models.CharField(max_length=50)),
                ('nearest_market_church_hospital', models.CharField(max_length=50)),
                ('customer_email', models.CharField(max_length=50, null=True)),
                ('contract_number', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='MainStorage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_imei', models.CharField(max_length=15, unique=True)),
                ('phone_type', models.CharField(choices=[('S18 (4+64)', 'S18 (4+64)'), ('A60 (2+32)', 'A60 (2+32)'), ('A04 (2+32)', 'A04 (2+32)'), ('A18 (1+32)', 'A18 (1+32)'), ('Camon 20 (8+256)', 'Camon 20 (8+256)'), ('Camon 19 (4+128)', 'Camon 19 (4+128)'), ('Spark 10 (8+128)', 'Spark 10 (8+128)'), ('Spark 10C (8+128)', 'Spark 10C (8+128)'), ('Spark 10C (4+128)', 'Spark 10C (4+128)'), ('Spark 8C (2+64)', 'Spark 8C (2+64)'), ('Pop 7 pro (4+64)', 'Pop 7 pro (4+64)'), ('Pop 7 pro (3+64)', 'Pop 7 pro (3+64)'), ('Pop 7 (2+64)', 'Pop 7 (2+64)')], default='S18 (4+64)', max_length=25)),
                ('in_stock', models.BooleanField(default=True)),
                ('sales_type', models.CharField(max_length=10, null=True)),
                ('contract_no', models.CharField(max_length=8, null=True)),
                ('entry_date', models.DateField()),
                ('stock_out_date', models.DateField()),
                ('assigned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='phone_reference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=30)),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('merchant_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='PhoneData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_type', models.CharField(choices=[('S18 (4+64)', 'S18 (4+64)'), ('A60 (2+32)', 'A60 (2+32)'), ('A04 (2+32)', 'A04 (2+32)'), ('A18 (1+32)', 'A18 (1+32)'), ('Camon 20 (8+256)', 'Camon 20 (8+256)'), ('Camon 19 (4+128)', 'Camon 19 (4+128)'), ('Spark 10 (8+128)', 'Spark 10 (8+128)'), ('Spark 10C (8+128)', 'Spark 10C (8+128)'), ('Spark 10C (4+128)', 'Spark 10C (4+128)'), ('Spark 8C (2+64)', 'Spark 8C (2+64)'), ('Pop 7 pro (4+64)', 'Pop 7 pro (4+64)'), ('Pop 7 pro (3+64)', 'Pop 7 pro (3+64)'), ('Pop 7 (2+64)', 'Pop 7 (2+64)')], default='S18 (4+64)', max_length=25)),
                ('imei_number', models.CharField(max_length=15, unique=True)),
                ('selling_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('cost_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_period', models.CharField(max_length=50, null=True)),
                ('deposit', models.DecimalField(decimal_places=2, max_digits=10)),
                ('paid', models.BooleanField(default=False)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptic_core_app.agentprofile')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptic_core_app.customerdata')),
            ],
        ),
        migrations.CreateModel(
            name='AgentStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imei_number', models.CharField(max_length=15, unique=True)),
                ('phone_type', models.CharField(blank=True, max_length=25)),
                ('collection_date', models.DateField()),
                ('sales_type', models.CharField(choices=[('Cash', 'Cash'), ('Loan', 'Loan')], default='Loan', max_length=10)),
                ('in_stock', models.BooleanField(default=True)),
                ('stock_out_date', models.DateField()),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cryptic_core_app.agentprofile')),
            ],
        ),
    ]
