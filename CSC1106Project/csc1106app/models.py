# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class MyModel(models.Model):
    name = models.CharField(max_length = 100)
    description = models.TextField()

    def str(self):
        return self.name

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)
    employee = models.ForeignKey('Employee', on_delete=models.SET_NULL, null = True, blank=True, related_name='departments_managed')

    def str(self):
        return self.department_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def str(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    time_in = models.DateTimeField()
    time_out = models.DateTimeField(null=True, blank=True)

class Leave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start_date = models.DateField()
    leave_end_date = models.DateField()

class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.IntegerField()
    bonus = models.IntegerField()
    benefit = models.CharField(max_length=255)
    net_pay = models.IntegerField()