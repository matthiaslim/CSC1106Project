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
        fields = ['user', 'first_name', 'last_name', 'department', 'job_title', 'email', 'gender', 'date_of_birth',
                  'hire_date', 'contract_expiry_date', 'employee_role']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department':  forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'gender': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'class': 'form-control'}),
            'contract_expiry_date': forms.DateInput(attrs={'class': 'form-control'}),
            'employee_role': forms.TextInput(attrs={'class': 'form-control'}),

        }


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


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_description',
            'product_category',
            'product_quantity',
            'product_sale_price',
            'product_location',
            'product_width',
            'product_height',
            'product_length',
            'product_image'
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_description': forms.Textarea(attrs={'class': 'form-control',
                                                         'rows': 3}),
            'product_category': forms.Select(attrs={'class': 'form-control'}, choices=[
                ("Bar Furniture", "Bar Furniture"),
                ("Beds", "Beds"),
                ("Bookcases & shelving units", "Bookcases & shelving units"),
                ("Cabinets & cupboards", "Cabinets & cupboards"),
                ("Chairs", "Chairs"),
                ("Nursery furniture", "Nursery furniture"),
                ("Wardrobes", "Wardrobes")
            ]),
            'product_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_location': forms.TextInput(attrs={'class': 'form-control'}),
            'product_width': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_height': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_image': forms.TextInput(attrs={'class': 'form-control'}),
        }
