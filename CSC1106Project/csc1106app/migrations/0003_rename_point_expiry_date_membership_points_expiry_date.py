# Generated by Django 4.2.13 on 2024-07-08 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('csc1106app', '0002_alter_membership_phone_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='point_expiry_date',
            new_name='points_expiry_date',
        ),
    ]