from django.contrib import admin
from .models import (Attendance,Department,Employee,Invoice,
                    InvoiceProduct,Leave,LeaveBalance, Membership,Payroll,
                    Product,Transaction,TransactionProduct,User);


# Register your models here.
models = [Attendance, Department, Employee, Invoice, InvoiceProduct,
            Leave, LeaveBalance, Membership, Payroll, Product, Transaction,TransactionProduct,
            User]

for model in models:
    admin.site.register(model)