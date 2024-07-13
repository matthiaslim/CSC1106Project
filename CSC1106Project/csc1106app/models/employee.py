from django.db import models
from .user import User
from .department import Department


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null = True, blank=True, related_name='employees')
    job_title = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    contract_expiry_date = models.DateField(null=True, blank=True)
    employee_role = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"