from django.forms import inlineformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .crud_ops import *
from .forms import *

from datetime import datetime

# Home View
def index(request):
    return render(request, 'index.html')


# Login View
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or another page after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page or another page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


# Inventory Views
@login_required
def inventory_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Management', 'url': '/inventory/management/'}]
    return render(request, 'inventory_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory'})


@login_required
def inventory_statistics(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Statistics', 'url': '/inventory/statistics/'}]
    return render(request, 'inventory_statistics.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory Statistics'})


# Customer Views
@login_required
def customer_management(request):
    memberships = Membership.objects.all()
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    data =  {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'memberships': memberships}
    return render(request, 'customer/customer_management.html', data)


@login_required
def customer_details(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
    except Membership.DoesNotExist:
        # Handle the case where the customer does not exist
        membership = None

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                   {'title': f'Customer Details - {membership}'}]
    data =  {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'membership': membership}

    return render(request, 'customer/customer_details.html', data)


@login_required
def create_customer(request):

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            dob = form.cleaned_data.get('dob')
            country = form.cleaned_data.get('country')
            status = form.cleaned_data.get('status')
            age = form.cleaned_data.get('age')
            address = form.cleaned_data.get('address')
            # call a func to save the data

            # m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address, phone_number=phone_number, dob=dob, country=country, status=status, age=age, address=address)
            # m1.save()
            m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address, 
                            phone_number=phone_number, point_expiry_date=dob, member_expiry_date=datetime.now(), 
                            membership_status=status, points=0, membership_level="Bronze", address=address)
            m1.save()
            return redirect('customer_management')
    else:
        form = CreateCustomerForm()
        
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer', 'form': form})

# Employee Views
def employee_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'first_name')
    order = request.GET.get('order', 'asc')
    employees = search_and_filter_employees(query, sort_by, order)
    return render(request, 'hrms/employee_list.html', {'employees': employees, 'query': query, 'sort_by': sort_by, 'order': order})

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'hrms/employee_detail.html', {'employee': employee})

def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    return render(request, 'hrms/employee_form.html', {'form': form})

def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', employee_id=employee.employee_id)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hrms/employee_form.html', {'form': form})

def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.delete()
    return redirect('employee_list')

# Department Views
def department_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'department_name')
    order = request.GET.get('order', 'asc')
    departments = search_and_filter_departments(query, sort_by, order)
    return render(request, 'hrms/department_list.html', {'departments': departments, 'query': query, 'sort_by': sort_by, 'order': order})


def department_detail(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    return render(request, 'hrms/department_detail.html', {'department': department})

def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hrms/department_form.html', {'form': form})

def department_update(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_detail', department_id=department.id)
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'hrms/department_form.html', {'form': form})

def department_delete(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')

# Attendance Views
def attendance_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'attendance_date')
    order = request.GET.get('order', 'asc')
    attendances = search_and_filter_attendances(query, sort_by, order)
    return render(request, 'hrms/attendance_list.html', {'attendances': attendances, 'query': query, 'sort_by': sort_by, 'order': order})

def attendance_create(request):
    if request.method == "POST":
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    return render(request, 'hrms/attendance_form.html', {'form': form})

def attendance_update(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'hrms/attendance_form.html', {'form': form})

def attendance_delete(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    attendance.delete()
    return redirect('attendance_list')

# Leave Views
def leave_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'leave_start_date')
    order = request.GET.get('order', 'asc')
    leaves = search_and_filter_leaves(query, sort_by, order)
    return render(request, 'hrms/leave_list.html', {'leaves': leaves, 'query': query, 'sort_by': sort_by, 'order': order})

def leave_create(request):
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()
    return render(request, 'hrms/leave_form.html', {'form': form})

def leave_update(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.method == "POST":
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveForm(instance=leave)
    return render(request, 'hrms/leave_form.html', {'form': form})

def leave_delete(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    leave.delete()
    return redirect('leave_list')

# Payroll Views
def payroll_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'employee__first_name')
    order = request.GET.get('order', 'asc')
    payrolls = search_and_filter_payrolls(query, sort_by, order)
    return render(request, 'hrms/payroll_list.html', {'payrolls': payrolls, 'query': query, 'sort_by': sort_by, 'order': order})

def payroll_create(request):
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'hrms/payroll_form.html', {'form': form})

def payroll_update(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    if request.method == "POST":
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm(instance=payroll)
    return render(request, 'hrms/payroll_form.html', {'form': form})

def payroll_delete(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    payroll.delete()
    return redirect('payroll_list')

# Finance Views
def sales_management(request):
    return render(request, 'finance/sales_management.html')

def create_sales(request):
    if request.method == 'POST':
        sales_form = SalesForm(request.POST)
        formset = SalesProductFormSet(request.POST, request.FILES)
        print(formset.errors)
        if sales_form.is_valid() and formset.is_valid():
            sales = sales_form.save()
            formset.instance = sales
            formset.save()
            return redirect('sales_management')
    else:
        sales_form = SalesForm()
        formset = SalesProductFormSet()

    for form in formset.forms:
        form.set_initial_price()

    return render(request, 'finance/create_sales.html', {'sales_form': sales_form , 'formset': formset})

def invoice_management(request):
    return render(request, 'finance/invoice_management.html')

def create_invoice(request):
    if request.method == 'POST':
        invoice_form = InvoiceForm(request.POST)
        formset = InvoiceProductFormSet(request.POST)
        if invoice_form.is_valid() and formset.is_valid():
            invoice = invoice_form.save()
            formset.instance = invoice
            formset.save()
            return redirect('invoice_management')
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceProductFormSet()


    return render(request, 'finance/create_invoice.html', {'invoice_form': invoice_form, 'formset': formset})

def get_product_price(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.product_sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)