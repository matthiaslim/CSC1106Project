from django.db import models
from .user import User
from .department import Department


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    contract_expiry_date = models.DateField()
    employee_role = models.CharField(max_length=20)