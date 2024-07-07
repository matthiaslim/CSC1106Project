from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import inlineformset_factory, Select

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

    country = forms.ChoiceField(label="Country",
                                choices=[('Singapore', 'Singapore'), ('Malaysia', 'Malaysia'), ('China', 'China')])
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


class InvoiceForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]



    employee_id = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Employee", to_field_name="employee_id")
    status = forms.ChoiceField(choices=STATUS_CHOICES, initial='pending', label="Status",
                               widget=forms.Select(attrs={'class': 'form-select'}))
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    class Meta:
        model = Invoice
        fields = ['employee_id', 'invoice_date', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_id'].widget.attrs.update({'class': 'form-select'})


class CustomSelect(Select):
    def __init__(self, attrs=None, choices=(), prices=None):
        default_attrs = {'class': 'form-select'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, choices)

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        display_name = label[0] if isinstance(label, tuple) and len(label) == 2 else label
        data_price = label[1] if isinstance(label, tuple) and len(label) == 2 else None

        option = super().create_option(name, value, display_name, selected, index, subindex=subindex, attrs=attrs)

        if data_price:
            option['attrs']['data-price'] = data_price

        return option

    def optgroups(self, name, value, attrs=None):
        groups = []
        for index, (option_value, option_label) in enumerate(self.choices):
            if isinstance(option_label, (list, tuple)) and len(option_label) == 2:
                group_name = None
                subgroup = [
                    self.create_option(name, option_value, option_label, option_value in value, index, attrs=attrs)]
                groups.append((group_name, subgroup, index))
        return groups


class InvoiceProductForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque')
    ]
    products = Product.objects.all()
    product_items = [(product.product_id, (product.product_name, product.product_sale_price)) for product in
                     products]

    # product_id = forms.ModelChoiceField(queryset=Product.objects.none(), label="Product", to_field_name="product_id")
    payment_terms = forms.ChoiceField(choices=PAYMENT_CHOICES, initial='card', label="Status",
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    product_id = forms.ChoiceField(choices=product_items, widget=CustomSelect)
    invoice_price_per_unit = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}))

    class Meta:
        model = InvoiceProduct
        fields = ['product_id', 'invoice_quantity', 'invoice_price_per_unit', 'payment_terms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['invoice_quantity'].widget.attrs.update({'class': 'form-control'})
        # self.fields['invoice_price_per_unit'].widget.attrs.update({'class': 'form-control'})


InvoiceProductFormSet = inlineformset_factory(
    Invoice, InvoiceProduct,
    form=InvoiceProductForm,
    fields=('product_id', 'invoice_quantity', 'invoice_price_per_unit', 'payment_terms'), extra=1, can_delete=True)
