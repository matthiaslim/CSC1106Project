import os

from django.db.models.signals import post_save, post_delete, pre_save, post_delete
from django.dispatch import receiver
from .models import Employee, LeaveBalance, Transaction, Invoice
from django.conf import settings

from .models import Employee, LeaveBalance, Product, Attendance
import os
import shutil
from django.conf import settings
from datetime import datetime

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

def product_image_path(instance, filename):
    # Ensure that product_id is set before generating the file path
    if instance.product_id:
        return f'product_image/{instance.product_id}/{filename}'
    return f'product_image/temp/{filename}'

def attendance_path(instance, filename):
    dt = datetime.now()
    numeric_date = dt.strftime('%Y%m%d%H%M%S')
    if instance.attendance_id:
        return f'attendance_images/{instance.employee.employee_id}/{numeric_date}_{filename}'
    return f'attendance_images/tmp/{numeric_date}_{filename}'

@receiver(post_save, sender=Attendance)
def handle_post_save_attendance(sender, instance, created, **kwargs):
    if created:
        # Construct paths
        temp_path = os.path.join(settings.MEDIA_ROOT, 'attendance_images/tmp/', os.path.basename(instance.image.name))
        new_path = os.path.join(settings.MEDIA_ROOT, 'attendance_images/', str(instance.employee.employee_id), os.path.basename(instance.image.name))

        # Move the file if it exists
        if os.path.exists(temp_path):
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            shutil.move(temp_path, new_path)

            os.rmdir(os.path.join(settings.MEDIA_ROOT, 'attendance_images/tmp'))

            # Update the image field path
            instance.image.name = attendance_path(instance, os.path.basename(instance.image.name))
            instance.save()


@receiver(pre_save, sender=Product)
def handle_product_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            old_image = old_instance.product_image.name if old_instance.product_image else None
            new_image = instance.product_image.name
            
            if old_image and old_image != new_image:
                old_file_path = os.path.join(settings.MEDIA_ROOT, old_image)
                
                if os.path.isfile(old_file_path):
                    os.remove(old_file_path)
                    
                    directory = os.path.dirname(old_file_path)
                    while directory != settings.MEDIA_ROOT and not os.listdir(directory):
                        os.rmdir(directory)
                        directory = os.path.dirname(directory)

        except sender.DoesNotExist:
            pass

@receiver(post_save, sender=Product)
def update_image_path(sender, instance, created, **kwargs):
    if created or (instance.product_image and instance.product_image.name.startswith('product_image/temp/')):
        if instance.product_id:
            temp_path = os.path.join(settings.MEDIA_ROOT, 'product_image/temp/', os.path.basename(instance.product_image.name))
            new_path = os.path.join(settings.MEDIA_ROOT, 'product_image/', str(instance.product_id), os.path.basename(instance.product_image.name))
            
            if os.path.exists(temp_path):
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                shutil.move(temp_path, new_path)

                os.rmdir(os.path.join(settings.MEDIA_ROOT, 'product_image/temp/'))

            instance.product_image.name = product_image_path(instance, os.path.basename(instance.product_image.name))
            instance.save()

@receiver(post_delete, sender=Product)
def delete_image_file(sender, instance, **kwargs):
    if instance.product_image:
        file_path = os.path.join(settings.MEDIA_ROOT, instance.product_image.name)
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            
            directory = os.path.dirname(file_path)
            while directory != settings.MEDIA_ROOT and not os.listdir(directory):
                os.rmdir(directory)
                directory = os.path.dirname(directory)