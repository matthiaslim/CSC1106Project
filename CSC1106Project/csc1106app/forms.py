from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
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
            'department': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.Select(choices=JOB_TITLE_CHOICES, attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
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
        fields = ['first_name', 'last_name', 'email_address', 'phone_number', 'date_of_birth', 'country',
                  'membership_status', 'gender', 'address']
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

    payment_terms = forms.ChoiceField(choices=PAYMENT_CHOICES, initial='card', label="Status",
                                      widget=forms.Select(attrs={'class': 'form-select'}))
    invoice_price_per_unit = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'disabled': True}))

    class Meta:
        model = InvoiceProduct
        fields = ['product_id', 'invoice_quantity', 'invoice_price_per_unit', 'payment_terms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the products and generate the product items list dynamically
        products = Product.objects.all()
        product_items = [(product.product_id, f"{product.product_name} - ${product.product_sale_price}") for product in
                         products]

        # Set the product_id field dynamically
        self.fields['product_id'] = forms.ChoiceField(choices=product_items,
                                                      widget=CustomSelect(attrs={'class': 'form-control'}))

        # Add class to invoice_quantity field
        self.fields['invoice_quantity'].widget.attrs.update({'class': 'form-control'})


InvoiceProductFormSet = inlineformset_factory(
    Invoice, InvoiceProduct,
    form=InvoiceProductForm,
    fields=('product_id', 'invoice_quantity', 'invoice_price_per_unit', 'payment_terms'), extra=1, can_delete=True)


class SalesForm(forms.ModelForm):
    membership_id = forms.ModelChoiceField(queryset=Membership.objects.all(), label="Member", to_field_name="member_id")
    employee_id = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Employee", to_field_name="employee_id")
    transaction_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    points_earned = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Transaction
        fields = ['membership_id', 'employee_id', 'transaction_date', 'points_earned']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['membership_id'].widget.attrs.update({'class': 'form-select'})
        self.fields['employee_id'].widget.attrs.update({'class': 'form-select'})
        self.fields['points_earned'].widget.attrs.update({'class': 'form-select'})


class SelectWOA(Select):
    # Referenced from: https://stackoverflow.com/questions/5089396/django-form-field-choices-adding-an-attribute/56097149#56097149
    def __init__(self, attrs=None, choices=()):
        default_attrs = {'class': 'form-select'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs, choices)

    def create_option(self, name, value, label, selected, index,
                      subindex=None, attrs=None):
        if isinstance(label, dict):
            opt_attrs = label.copy()
            label = opt_attrs.pop('label')
        else:
            opt_attrs = {}
        option_dict = super(SelectWOA, self).create_option(name, value,
                                                           label, selected, index, subindex=subindex, attrs=attrs)
        for key, val in opt_attrs.items():
            option_dict['attrs'][key] = val
        return option_dict


class SalesProductForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('cheque', 'Cheque')
    ]

    payment_terms = forms.ChoiceField(choices=PAYMENT_CHOICES, initial='card', label="Payment Terms",
                                      widget=forms.Select(attrs={'class': 'form-select'}))

    transaction_price_per_unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control disabled', 'readonly': True}))

    class Meta:
        model = TransactionProduct
        fields = ['product_id', 'transaction_quantity', 'transaction_price_per_unit', 'payment_terms']

    def __init__(self, *args, **kwargs):
        super(SalesProductForm, self).__init__(*args, **kwargs)

        # Dynamically populate the product choices
        products = Product.objects.all()
        product_items = [(product.product_id, f"{product.product_name} - ${product.product_sale_price}") for product in
                         products]

        self.fields['product_id'] = forms.ChoiceField(
            choices=product_items,
            label="Product",
            widget=forms.Select(attrs={'class': 'form-select product-select'})
        )

        self.fields['transaction_quantity'].widget.attrs.update({'class': 'form-control'})
        self.fields['transaction_price_per_unit'].widget.attrs.update(
            {'class': 'form-control price-per-unit', 'readonly': True}
        )
        self.fields['payment_terms'].widget.attrs.update({'class': 'form-select'})

        self.set_initial_price()

    def set_initial_price(self):
        if self.is_bound and 'product_id' in self.data:
            try:
                product_id = int(self.data.get('product_id'))
                product = Product.objects.get(pk=product_id)
                self.fields['transaction_price_per_unit'].initial = product.product_sale_price
            except (ValueError, Product.DoesNotExist):
                pass
        elif self.initial.get('product_id'):
            product_id = self.initial['product_id']
            product = Product.objects.get(pk=product_id)
            self.fields['transaction_price_per_unit'].initial = product.product_sale_price

    def clean(self):
        cleaned_data = super().clean()
        product_id = cleaned_data.get("product_id")

        try:
            product_instance = Product.objects.get(pk=product_id)
            cleaned_data['product_id'] = product_instance
        except Product.DoesNotExist:
            raise ValidationError({"product_id": "Invalid product ID. Product does not exist."})

        return cleaned_data


SalesProductFormSet = inlineformset_factory(
    Transaction,
    TransactionProduct,
    form=SalesProductForm,
    fields=('product_id', 'transaction_quantity', 'transaction_price_per_unit', 'payment_terms'),
    extra=1,
    can_delete=True
)
