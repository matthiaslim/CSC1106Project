from django.db.models import Q
from .models import *

def search_and_filter_employees(query=None, sort_by='first_name', order='asc'):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    employees = Employee.objects.all()

    if query:
        employees = employees.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(department__department_name__icontains=query)
        )
    
    employees = employees.order_by(sort_by)
    return employees

def search_and_filter_departments(query=None, sort_by='department_name', order='asc'):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    departments = Department.objects.all()

    if query:
        departments = departments.filter(
            Q(department_name__icontains=query) |
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query)
        )
    
    departments = departments.order_by(sort_by)
    return departments

def search_and_filter_attendances(query=None, sort_by='employee__first_name', order='asc'):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    attendances = Attendance.objects.all()

    if query:
        attendances = attendances.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query)
        )
    
    attendances = attendances.order_by(sort_by)
    return attendances

def search_and_filter_leaves(query=None, sort_by='leave_start_date', order='asc'):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    leaves = Leave.objects.all()

    if query:
        leaves = leaves.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(leave_start_date__icontains=query) |
            Q(leave_end_date__icontains=query)
        )
    
    leaves = leaves.order_by(sort_by)
    return leaves


def search_and_filter_payrolls(query=None, sort_by='first_name', order='asc'):
    if order == 'desc':
        sort_by = f'-{sort_by}'
    
    payrolls = Payroll.objects.all()

    if query:
        employees = employees.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(salary__icontains=query) |
            Q(net_pay__icontains=query) 
        )
    
    payrolls = payrolls.order_by(sort_by)
    return payrolls
