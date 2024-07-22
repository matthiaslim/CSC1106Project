import uuid

from django.db import models
from .employee import Employee
from datetime import date


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    PAYMENT_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque')
    ]
    
    invoice_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    payment_due_date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    payment_terms = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='Card')
    uuid_filename = models.UUIDField(default=uuid.uuid4, editable=False)

    def total_value(self):
        return sum([invoice_product.invoice_quantity * invoice_product.invoice_price_per_unit for invoice_product in self.invoiceproduct_set.all()])

