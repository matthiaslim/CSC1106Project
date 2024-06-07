from django.db import models
from .employee import Employee

class EmployeeAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()