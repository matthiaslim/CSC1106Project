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
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    hire_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    contract_expiry_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Employee
        fields = ['user', 'first_name', 'last_name', 'department', 'job_title', 'email', 'gender', 'date_of_birth',
                  'hire_date', 'contract_expiry_date', 'employee_role']
        
        GENDER_CHOICES = [
            ('', 'Select a gender'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ]

        JOB_TITLE_CHOICES = [
            ('', 'Select a title'),
            ('manager', 'Manager'),
            ('employee', 'Employee'),
            ('hr', 'HR'),
        ]

        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'department':  forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.Select(choices=JOB_TITLE_CHOICES, attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'gender': forms.Select(choices=GENDER_CHOICES, attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contract_expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'employee_role': forms.TextInput(attrs={'class': 'form-control'}),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'employee']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['time_out']


class LeaveAddForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['employee', 'leave_start_date', 'leave_end_date', 'leave_type']

        LEAVE_TYPE = [
                ('Annual', 'Annual'),
                ('Medical', 'Medical'),
            ]

        widgets = {
                'leave_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'leave_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                'leave_type': forms.Select(choices=LEAVE_TYPE, attrs={'class': 'form-control'}),
            }

class LeaveStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_status', 'remark']

        STATUS_CHOICES = [
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Denied', 'Denied'),
        ]

        widgets = {
            'leave_status': forms.Select(choices=STATUS_CHOICES, attrs={'class': 'form-control'}),
            'remark': forms.TextInput(attrs={'class': 'form-control'}),
        }


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
            'product_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


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
