# Generated by Django 4.2.13 on 2024-06-14 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('csc1106app', '0002_rename_products_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('attendance_date', models.DateField()),
                ('time_in', models.DateTimeField()),
                ('time_out', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='EmployeeLeave',
            new_name='Leave',
        ),
        migrations.RenameField(
            model_name='leave',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RenameField(
            model_name='leave',
            old_name='leave_end',
            new_name='leave_end_date',
        ),
        migrations.RenameField(
            model_name='leave',
            old_name='leave_start',
            new_name='leave_start_date',
        ),
        migrations.RenameField(
            model_name='payroll',
            old_name='employee_id',
            new_name='employee',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='department_id',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='payroll',
            name='date_of_month',
        ),
        migrations.AddField(
            model_name='department',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments_managed', to='csc1106app.employee'),
        ),
        migrations.AddField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='csc1106app.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='employee',
            name='contract_expiry_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='employee_role',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='gender',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='benefit',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='bonus',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='net_pay',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='payroll',
            name='salary',
            field=models.IntegerField(),
        ),
        migrations.DeleteModel(
            name='EmployeeAttendance',
        ),
        migrations.AddField(
            model_name='attendance',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='csc1106app.employee'),
        ),
    ]
