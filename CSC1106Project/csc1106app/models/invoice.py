from django.db import models
from .employee import Employee


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    status = models.CharField(max_length=50)
