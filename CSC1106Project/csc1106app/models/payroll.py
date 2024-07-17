from django.db import models
from datetime import date
from decimal import Decimal
from .employee import Employee

class Payroll(models.Model):

    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    month = models.DateField(default=date.today)
    hours_worked = models.FloatField(default=0.0)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    cpf_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Payroll for {self.employee} for {self.month}"