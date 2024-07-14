from django.db import models
from .employee import Employee

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()
    leave_status = models.CharField(max_length=10, default = "pending")
    remark = models.TextField(blank = True, null = True)
    leave_type = models.CharField(max_length=10, default = "annual")

    def __str__(self):
        return f"{self.leave_id} {self.employee}"