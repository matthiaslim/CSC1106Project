from django.db import models
from .employees import Employee

class EmployeeLeave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start = models.DateField()
    leave_end = models.DateField()
