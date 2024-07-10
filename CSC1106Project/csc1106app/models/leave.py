from django.db import models
from .employee import Employee

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    leave_status = models.CharField(max_length=7, default="pending")

    def __str__(self):
        return f"Leave {self.leave_id} for {self.employee}"