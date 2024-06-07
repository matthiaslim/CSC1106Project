from django.contrib import admin
from .models import (EmployeeAttendance,Department,Employee,Invoice,
                    InvoiceProduct,EmployeeLeave,Membership,Payroll,
                    Products,Transaction,TransactionProduct,User);


# Register your models here.
models = [ EmployeeAttendance, Department, Employee, Invoice, InvoiceProduct,
            EmployeeLeave, Membership, Payroll, Products, Transaction,TransactionProduct,
            User]

for model in models:
    admin.site.register(model)