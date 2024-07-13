from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import *
from .crud_ops import *
from .forms import *
import os
from django.core.files.storage import FileSystemStorage
from CSC1106Project import settings;



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
    # Fetch all products initially
    products = Product.objects.all()

    # Handle filtering based on request parameters
    product_name = request.GET.get('product_name')
    product_category = request.GET.get('product_category')
    product_location = request.GET.get('product_location')

    if product_name:
        products = products.filter(product_name__icontains=product_name)
    if product_category:
        products = products.filter(product_category__icontains=product_category)
    if product_location:
        products = products.filter(product_location__icontains=product_location)

    return render(request, 'inventory/inventory_management.html', {'products': products})


@login_required
def inventory_statistics(request):
    return render(request, 'inventory/inventory_statistics.html')


def add_product(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Manage', 'url': '/inventory/management'},
                   {'title': 'Add Product', 'url': '/inventory/management/create'}, ]
    
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid:
            if 'product_image' in request.FILES:
                img = request.FILES['product_image']
            
                upload_dir = os.path.join(settings.BASE_DIR, 'CSC1106Project','static', 'img', 'upload')

                if not os.path.exists(upload_dir):
                    os.makedirs(upload_dir)

                file_path = os.path.join(upload_dir,img.name)
                
                with open(file_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                print(f"Saved image: {file_path}")  # Debugging statement


                form.save()

            return redirect('inventory_management')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'breadcrumbs': breadcrumbs, 'form': form})

@login_required
def get_product(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        product_dict = model_to_dict(product)
        return JsonResponse({'product': product_dict , 'status' : 200})
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500})

@login_required
def update_product(request, pk):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Manage', 'url': '/inventory/management'},
                   {'title': 'Update Product', 'url': '/inventory/management/update/<int:pk>'}, ]
    product = get_object_or_404(Product, pk=pk)
    # Handle the update logic here
    return render(request, 'inventory/update_product.html', {'product': product, 'breadcrumbs': breadcrumbs})


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        if request.method == 'DELETE':
            product.delete()
        return JsonResponse({'status': 200, 'message': 'Product deleted successfully.'})
    except:
        return JsonResponse({'status': 400, 'message': 'Bad request.'})




# Customer Views
@login_required
def customer_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    return render(request, 'customer/customer_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Customers'})


@login_required
def customer_details(request, customerID):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                   {'title': f'Customer Details - {customerID}'}]
    return render(request, 'customer/customer_details.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': f'Customer Details - {customerID}'})


@login_required
def create_customer(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer'})


# Employee Views
def employee_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'first_name')
    order = request.GET.get('order', 'asc')
    employees = search_and_filter_employees(query, sort_by, order)

    return render(request, 'hrms/employee_list.html', {
        'employees': employees,
        'query': query,
        'sort_by': sort_by,
        'order': order,
    })


def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'hrms/employee_detail.html', {'employee': employee})


def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('employee_list')
            except IntegrityError:
                form.add_error(None, "An employee with this user already exists.")
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
    return render(request, 'hrms/department_list.html',
                  {'departments': departments, 'query': query, 'sort_by': sort_by, 'order': order})


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
            return redirect('department_detail', department_id=department.department_id)
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
    return render(request, 'hrms/attendance_list.html',
                  {'attendances': attendances, 'query': query, 'sort_by': sort_by, 'order': order})


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
    return render(request, 'hrms/leave_list.html',
                  {'leaves': leaves, 'query': query, 'sort_by': sort_by, 'order': order})


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
    return render(request, 'hrms/payroll_list.html',
                  {'payrolls': payrolls, 'query': query, 'sort_by': sort_by, 'order': order})


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
