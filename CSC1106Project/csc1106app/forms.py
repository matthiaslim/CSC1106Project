from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')

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


class CreateCustomerForm(forms.ModelForm):
    class Meta:
        model = Membership
        fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'date_of_birth', 'country', 'membership_status', 'gender', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'country': forms.Select(),
            'membership_status': forms.Select(),
            'gender': forms.Select(),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email_address': 'Email',
            'phone_number': 'Phone Number',
            'date_of_birth': 'Date of Birth',
            'country': 'Country',
            'membership_status': 'Status',
            'gender': 'Gender',
            'address': 'Address',
        }

    def __init__(self, *args, **kwargs):
        super(CreateCustomerForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].max_length = 100
        self.fields['last_name'].max_length = 100
        self.fields['email_address'].max_length = 100
        self.fields['address'].max_length = 100
