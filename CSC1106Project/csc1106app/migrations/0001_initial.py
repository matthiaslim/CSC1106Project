# Generated by Django 4.2.13 on 2024-06-11 15:23

import csc1106app.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(blank=True, default='', max_length=254, unique=True)),
                ('name', models.CharField(blank=True, default='', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', csc1106app.models.user.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('department_id', models.AutoField(primary_key=True, serialize=False)),
                ('department_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('employee_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('job_title', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('gender', models.CharField(max_length=20)),
                ('date_of_birth', models.DateField()),
                ('hire_date', models.DateField()),
                ('contract_expiry_date', models.DateField()),
                ('employee_role', models.CharField(max_length=20)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.department')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=55)),
                ('email_address', models.EmailField(max_length=100)),
                ('country', models.CharField(max_length=200)),
                ('membership_level', models.CharField(max_length=50)),
                ('points', models.IntegerField()),
                ('point_expiry_date', models.DateField()),
                ('member_expiry_date', models.DateField()),
                ('membership_status', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.CharField(max_length=255)),
                ('product_category', models.CharField(max_length=255)),
                ('product_quantity', models.IntegerField()),
                ('product_sale_price', models.FloatField()),
                ('product_location', models.CharField(max_length=50)),
                ('product_width', models.IntegerField()),
                ('product_height', models.IntegerField()),
                ('product_length', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('transaction_id', models.AutoField(primary_key=True, serialize=False)),
                ('points_earned', models.IntegerField()),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee')),
                ('membership_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.membership')),
            ],
        ),
        migrations.CreateModel(
            name='TransactionProduct',
            fields=[
                ('transaction_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('transaction_quantity', models.IntegerField()),
                ('transaction_price_per_unit', models.FloatField()),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.products')),
                ('transaction_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.transaction')),
            ],
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('payroll_id', models.AutoField(primary_key=True, serialize=False)),
                ('salary', models.FloatField()),
                ('bonus', models.FloatField()),
                ('net_pay', models.FloatField()),
                ('date_of_month', models.DateTimeField()),
                ('benefit', models.CharField(max_length=50)),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceProduct',
            fields=[
                ('invoice_product_id', models.AutoField(primary_key=True, serialize=False)),
                ('invoice_quantity', models.IntegerField()),
                ('invoice_price_per_unit', models.FloatField()),
                ('payment_terms', models.CharField(max_length=30)),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.invoice')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.products')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeLeave',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_start', models.DateField()),
                ('leave_end', models.DateField()),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAttendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('time_in', models.TimeField()),
                ('time_out', models.TimeField()),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee')),
            ],
        ),
    ]
