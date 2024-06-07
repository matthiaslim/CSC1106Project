from django.db import models
from .employee import Employee

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.FloatField()
    bonus = models.FloatField()
    net_pay = models.FloatField()
    date_of_month = models.DateTimeField()
    benefit = models.CharField(max_length=50)
