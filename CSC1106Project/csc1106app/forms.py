from django import forms
from .models import *

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['user', 'first_name', 'last_name', 'department', 'job_title', 'email', 'gender', 'date_of_birth', 'hire_date', 'contract_expiry_date', 'employee_role']

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'employee']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'attendance_date', 'time_in', 'time_out']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_start_date', 'leave_end_date']

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'salary', 'bonus', 'benefit', 'net_pay']
