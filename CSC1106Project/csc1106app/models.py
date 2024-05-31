from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.AutoField(primary_key=True, null=False)
    username = models.CharField(max_length=50, null=False)
    password = models.CharField(max_length=50, null=False)
    salt = models.CharField(max_length=50, null=False)


class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=50)


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
    # i dont think we need employee_role?


class Payroll(models.Model):
    payroll_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.FloatField()
    bonus = models.FloatField()
    net_pay = models.FloatField()
    date_of_month = models.DateTimeField()
    benefit = models.CharField(max_length=50)


class EmployeeAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_date = models.DateField()
    time_in = models.TimeField()
    time_out = models.TimeField()


class EmployeeLeave(models.Model):
    leave_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_start = models.DateField()
    leave_end = models.DateField()


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_sale_price = models.FloatField()
    product_location = models.CharField(max_length=50)
    # Skipped out on image, width, height ,length


class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    invoice_date = models.DateField()
    status = models.CharField(max_length=50)


class InvoiceProduct(models.Model):
    invoice_product_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_quantity = models.IntegerField()
    invoice_price_per_unit = models.FloatField()
    payment_terms = models.CharField(max_length=30)


class Membership(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=55)
    email_address = models.EmailField(max_length=100)
    country = models.CharField(max_length=200)
    membership_level = models.CharField(max_length=50)
    points = models.IntegerField()
    point_expiry_date = models.DateField()
    member_expiry_date = models.DateField()
    membership_status = models.CharField(max_length=100)


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    points_earned = models.IntegerField()


class TransactionProduct(models.Model):
    transaction_product_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete=models.CASCADE)
    transaction_quantity = models.IntegerField()
    transaction_price_per_unit = models.FloatField()
