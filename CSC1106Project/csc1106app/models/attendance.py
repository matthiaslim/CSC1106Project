from django.db import models
from .employee import Employee
from django.utils import timezone

def attendance_path(instance, filename):
    dt = timezone.now()
    numeric_date = dt.strftime('%Y%m%d%H%M%S')
    if instance.attendance_id:
        return f'attendance_images/{instance.employee.employee_id}/{filename}'
    return f'attendance_images/tmp/{numeric_date}_{filename}'

class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)
    image = models.ImageField(upload_to=attendance_path, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} {self.time_in}"