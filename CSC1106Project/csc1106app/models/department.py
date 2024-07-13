from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null = True, blank=True, related_name='departments_managed')

    def __str__(self):
        return f"{self.department_name}"