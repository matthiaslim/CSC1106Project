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


class CreateCustomerForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=100)
    last_name = forms.CharField(label="Last Name", max_length=100)
    email_address = forms.EmailField(label="Email", max_length=100)
    phone_number = forms.IntegerField(label="Phone Number")

    dob = forms.DateField(label="Date of Birth", widget=forms.DateInput(attrs={'type': 'date'}))

    country = forms.ChoiceField(label="Country", choices=[('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'), ('China', 'China')])
    status = forms.ChoiceField(label="Status", choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    age = forms.IntegerField(label="Age", min_value=1, max_value=99)
    address = forms.CharField(label="Address", max_length=100)

    # def __init__(self, *args, **kwargs):
    #     super(CreateCustomerForm, self).__init__(*args, **kwargs)
    #     self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['email_address'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['dob'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['country'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['status'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['age'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['address'].widget.attrs.update({'class': 'form-control'})
