# Generated by Django 4.2.13 on 2024-07-15 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csc1106app', '0004_employee_onboarded'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
    ]
