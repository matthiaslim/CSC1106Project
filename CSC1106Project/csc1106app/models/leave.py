from django.db import models
from .employee import Employee

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()