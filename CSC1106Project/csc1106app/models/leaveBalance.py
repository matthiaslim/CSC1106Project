from django.db import models
from .employee import Employee

class LeaveBalance(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    annual_leave_balance = models.IntegerField(default=14)
    medical_leave_balance = models.IntegerField(default=365)

    def __str__(self):
        return f"{self.employee} - Annual: {self.annual_leave_balance}, Medical: {self.medical_leave_balance}"
