from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from datetime import date, timedelta
from .models import *

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email',]

        widgets = {
            'email': forms.EmailInput(attrs={'readonly': True, 'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class EmployeeForm(forms.ModelForm):
   

    GENDER_CHOICES = [
        ('', 'Select a gender'),
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    JOB_TITLE_CHOICES = [
        ('', 'Select a title'),
        ('Chairman', 'Chairman'),
        ('Manager', 'Manager'),
        ('Employee', 'Employee'),
        ('HR', 'HR'),
    ]

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.exclude(department_name='Chairman'), widget=forms.Select(attrs={'class': 'form-control'}))
    job_title = forms.ChoiceField(choices=JOB_TITLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    employee_role = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    date_of_birth = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    hire_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    contract_expiry_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].widget.attrs['max'] = (date.today() - (timedelta(days=6575))).isoformat()
        self.fields['hire_date'].widget.attrs['max'] = date.today().isoformat()
        self.fields['contract_expiry_date'].widget.attrs['min'] = date.today().isoformat()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'department', 'job_title', 'gender', 'date_of_birth',
                  'hire_date', 'contract_expiry_date', 'employee_role']
    

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'employee']


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['time_out']


class LeaveAddForm(forms.ModelForm):
    employee_name = forms.CharField(label='Employee Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
    employee_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Leave
        fields = ['employee_name', 'employee_id', 'leave_start_date', 'leave_end_date', 'leave_type']

        LEAVE_TYPE = [
            ('Annual', 'Annual'),
            ('Medical', 'Medical'),
        ]

        widgets = {
            'leave_start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'leave_type': forms.Select(choices=LEAVE_TYPE, attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        if 'employee' in initial:
            employee_instance = initial['employee']
            if employee_instance:
                initial['employee_name'] = f"{employee_instance.first_name} {employee_instance.last_name}"
                initial['employee_id'] = employee_instance.id
        super().__init__(*args, **kwargs)
        self.initial = initial


class LeaveStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['leave_id','leave_status', 'remark']

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
        fields = ['bonus']

    def save(self, *args, **kwargs):
        payroll = super().save(commit=False)
        payroll.net_pay = payroll.salary - payroll.cpf_deduction + payroll.bonus
        payroll.save()
        return payroll


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


class editProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_image',
            'product_description',
            'product_category',
            'product_sale_price',
            'product_location',
            'product_length',
            'product_width',
            'product_height',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'product_image': forms.FileInput(attrs={'class': 'form-control', "accept":".png, .jpg, .jpeg", "onchange":"validateFileType(this)"}),
            'product_description': forms.Textarea(attrs={'class': 'form-control',
                                                         'rows': 2}),
            'product_category': forms.Select(attrs={'class': 'form-control'}, choices=[
                ("Bar furniture", "Bar furniture"),
                ("Beds", "Beds"),
                ("Bookcases & shelving units", "Bookcases & shelving units"),
                ("Cabinets & cupboards", "Cabinets & cupboards"),
                ("Chairs", "Chairs"),
                ("Nursery furniture", "Nursery furniture"),
                ("Wardrobes", "Wardrobes")
            ]),
            'product_sale_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_location': forms.TextInput(attrs={'class': 'form-control'}),
            'product_length': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_width': forms.NumberInput(attrs={'class': 'form-control'}),
            'product_height': forms.NumberInput(attrs={'class': 'form-control'}),
        
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
    invoice_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    payment_due_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    payment_terms = forms.ChoiceField(label="Payment terms", widget=forms.Select(attrs={'class': 'form-select'}))
    employee_id = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Employee", to_field_name="employee_id")

    class Meta:
        model = Invoice
        fields = ['invoice_date', 'payment_due_date', 'payment_terms', 'employee_id']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['employee_id'].widget.attrs.update({'class': 'form-select'})
        self.fields['payment_terms'].choices = Invoice.PAYMENT_CHOICES

class InvoiceProductForm(forms.ModelForm):
    class Meta:
        model = InvoiceProduct
        fields = ['product_id', 'invoice_quantity', 'invoice_price_per_unit']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch the products and generate the product items list dynamically
        products = Product.objects.all()
        product_items = [(product.product_id, f"{product.product_name} - ${product.product_sale_price}") for product in
                         products]

        # Set the product_id field dynamically
        self.fields['product_id'] = forms.ModelChoiceField(queryset=Product.objects.all(),
                                                      widget=forms.Select(attrs={'class': 'form-select'}))

        # Add class to invoice_quantity field
        self.fields['invoice_quantity'].widget.attrs.update({'class': 'form-select'})
        self.fields['invoice_price_per_unit'].widget.attrs.update({'class': 'form-select'})




InvoiceProductFormSet = inlineformset_factory(
    Invoice, InvoiceProduct,
    form=InvoiceProductForm,
    fields=('product_id', 'invoice_quantity', 'invoice_price_per_unit'), extra=1, can_delete=True)


class SalesForm(forms.ModelForm):
    membership_id = forms.ModelChoiceField(queryset=Membership.objects.all(), label="Member", to_field_name="member_id")
    employee_id = forms.ModelChoiceField(queryset=Employee.objects.all(), label="Employee", to_field_name="employee_id")
    transaction_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    points_earned = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'true', 'value': 0}))
    payment_terms = forms.ChoiceField(label="Payment Terms", widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Transaction
        fields = ['membership_id', 'employee_id', 'transaction_date', 'points_earned', 'payment_terms']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['payment_terms'].choices = Transaction.PAYMENT_CHOICES
        self.fields['membership_id'].widget.attrs.update({'class': 'form-select'})
        self.fields['employee_id'].widget.attrs.update({'class': 'form-select'})
        self.fields['payment_terms'].widget.attrs.update({'class': 'form-select'})


class SalesProductForm(forms.ModelForm):

    transaction_price_per_unit = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control disabled', 'readonly': True}))

    class Meta:
        model = TransactionProduct
        fields = ['product_id', 'transaction_quantity', 'transaction_price_per_unit']

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

        self.fields['transaction_quantity'].widget.attrs.update({'class': 'form-control quantity', 'value': 1})
        self.fields['transaction_price_per_unit'].widget.attrs.update(
            {'class': 'form-control price-per-unit', 'readonly': True, 'value': products[0].product_sale_price}
        )
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
    fields=('product_id', 'transaction_quantity', 'transaction_price_per_unit'),
    extra=1,
    can_delete=True
)
