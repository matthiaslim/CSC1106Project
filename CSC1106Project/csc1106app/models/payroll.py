from django.db import models
from .employee import Employee

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.IntegerField()
    bonus = models.IntegerField()
    benefit = models.CharField(max_length=255)
    net_pay = models.IntegerField()
