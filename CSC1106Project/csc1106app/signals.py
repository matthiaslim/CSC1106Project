from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, LeaveBalance

@receiver(post_save, sender=Employee)
def create_leave_balance(sender, instance, created, **kwargs):
    if created:
        LeaveBalance.objects.create(employee=instance)
