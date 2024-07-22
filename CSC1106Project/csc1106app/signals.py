import os

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Employee, LeaveBalance, Transaction, Invoice
from django.conf import settings


@receiver(post_save, sender=Employee)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
        LeaveBalance.objects.create(employee=instance)


@receiver(post_delete, sender=Transaction)
def delete_sales_file(sender, instance, **kwargs):
    if instance.uuid_filename:
        file_path = os.path.join('media', 'sales', instance.transaction_date.strftime('%Y-%m-%d'),
                                     f"sales_{instance.uuid_filename}.pdf").replace('\\', '/')

        if os.path.isfile(file_path):
            os.remove(file_path)

            directory = os.path.dirname(file_path)
            while directory != settings.MEDIA_ROOT and not os.listdir(directory):
                os.rmdir(directory)
                directory = os.path.dirname(directory)

@receiver(post_delete, sender=Invoice)
def delete_invoice_file(sender, instance, **kwargs):
    if instance.uuid_filename:
        file_path = os.path.join('media', 'invoices', instance.invoice_date.strftime('%Y-%m-%d'),
                                     f"invoice_{instance.uuid_filename}.pdf").replace('\\', '/')

        if os.path.isfile(file_path):
            os.remove(file_path)

            directory = os.path.dirname(file_path)
            while directory != settings.MEDIA_ROOT and not os.listdir(directory):
                os.rmdir(directory)
                directory = os.path.dirname(directory)
