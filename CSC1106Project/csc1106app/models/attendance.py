from django.db import models
from .employee import Employee

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to='attendance_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.employee} {self.attendance_date}"