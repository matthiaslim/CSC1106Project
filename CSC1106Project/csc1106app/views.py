import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .crud_ops import *
from .forms import *
from .decorators import department_required
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
@department_required('Logistics')
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
@department_required('Logistics')
def inventory_statistics(request):
    return render(request, 'inventory/inventory_statistics.html')


@department_required('Logistics')
def add_product(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Manage', 'url': '/inventory/management'},
                   {'title': 'Add Product', 'url': '/inventory/management/create'}, ]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()

            return redirect('inventory_management')
    else:
        form = ProductForm()
    return render(request, 'inventory/add_product.html', {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@department_required('Logistics')
def get_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    try:
        product_image_url = product.product_image.url if product.product_image else None

        # Add or replace the product_image_url in the dictionary
        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'product_category': product.product_category,
            'product_quantity': product.product_quantity,
            'product_sale_price': product.product_sale_price,
            'product_location': product.product_location,
            'product_width': product.product_width,
            'product_height': product.product_height,
            'product_length': product.product_length,
            'product_image': product_image_url
        }

        return JsonResponse({'product': product_dict, 'status': 200})
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500})


@login_required
@department_required('Logistics')
def update_product(request, pk):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Manage', 'url': '/inventory/management'},
                   {'title': 'Update Product', 'url': '/inventory/management/update/<int:pk>'}, ]
    product = get_object_or_404(Product, pk=pk)
    # Handle the update logic here
    return render(request, 'inventory/update_product.html', {'product': product, 'breadcrumbs': breadcrumbs})


@login_required
@department_required('Logistics')
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
@department_required('Customer Relations')
def customer_management(request):
    memberships = Membership.objects.all()
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    data = {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'memberships': memberships}
    return render(request, 'customer/customer_management.html', data)


@login_required
@department_required('Customer Relations')
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
    data = {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'membership': membership}

    return render(request, 'customer/customer_details.html', data)


@login_required
@department_required('Customer Relations')
def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            country = form.cleaned_data.get('country')
            membership_status = form.cleaned_data.get('membership_status')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            # call a func to save the data

            # m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address, phone_number=phone_number, dob=dob, country=country, status=status, age=age, address=address)
            # m1.save()
            expiry_date = datetime.now() + relativedelta(years=1)
            m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address,
                            phone_number=phone_number, points_expiry_date=expiry_date, member_expiry_date=expiry_date,
                            membership_status=membership_status, points=0, membership_level="Bronze", address=address,
                            country=country, date_of_birth=date_of_birth, gender=gender)
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


@login_required
def update_customer(request, customerID):
    membership = Membership.objects.get(member_id=customerID)

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            membership.first_name = form.cleaned_data.get('first_name')
            membership.last_name = form.cleaned_data.get('last_name')
            membership.email_address = form.cleaned_data.get('email_address')
            membership.phone_number = form.cleaned_data.get('phone_number')
            membership.date_of_birth = form.cleaned_data.get('date_of_birth')
            membership.country = form.cleaned_data.get('country')
            membership.membership_status = form.cleaned_data.get('membership_status')
            membership.gender = form.cleaned_data.get('gender')
            membership.address = form.cleaned_data.get('address')
            membership.save()

            return redirect('customer_management')
    else:

        form = CreateCustomerForm(instance=membership)

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/update_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer', 'form': form})


@login_required
def delete_customer(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
        membership.delete()
    except Membership.DoesNotExist:
        # Handle the case where the customer does not exist
        membership = None

    return redirect('customer_management')


# Employee Views
# department_required('Human Resource')
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


# department_required('Human Resource')
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'hrms/employee_detail.html', {'employee': employee})


# department_required('Human Resource')
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


# department_required('Human Resource')
def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'hrms/employee_form.html', {'form': form})


# @department_required('Human Resource')
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        employee.delete()
        messages.success(request, 'Employee was deleted successfully.')
        return redirect('employee_list')


# Department Views
@department_required('Human Resource')
def department_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'department_name')
    order = request.GET.get('order', 'asc')
    departments = search_and_filter_departments(query, sort_by, order)
    return render(request, 'hrms/department_list.html',
                  {'departments': departments, 'query': query, 'sort_by': sort_by, 'order': order})


@department_required('Human Resource')
def department_detail(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    return render(request, 'hrms/department_detail.html', {'department': department})


@department_required('Human Resource')
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hrms/department_form.html', {'form': form})


@department_required('Human Resource')
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


@department_required('Human Resource')
def department_delete(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')


# Attendance Views
@login_required
def attendance_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'attendance_date')
    order = request.GET.get('order', 'asc')

    if sort_by == 'first_name':
        sort_by = 'employee__first_name'
    elif sort_by == 'last_name':
        sort_by = 'employee__last_name'

    attendances = search_and_filter_attendances(query, sort_by, order)
    return render(request, 'hrms/attendance_list.html',
                  {'attendances': attendances, 'query': query, 'sort_by': sort_by, 'order': order})


@login_required
def attendance_create(request):
    existing_attendance = Attendance.objects.filter(employee=request.user.employee, time_out__isnull=True).exists()
    if existing_attendance:
        messages.error(request, 'You have already checked in and have not checked out yet.')
        return redirect('attendance_list')

    if request.method == "POST":
        image_data = request.POST.get('image-data')
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]

            user_identifier = request.user.email

            data = ContentFile(base64.b64decode(imgstr), name=f'{user_identifier}_checkin.{ext}')

            try:
                employee = Employee.objects.get(user=request.user)
            except Employee.DoesNotExist:
                messages.error(request, 'Employee not found for the logged-in user.')
                return render(request, 'hrms/attendance_form.html')

            attendance = Attendance(
                employee=employee,  # Linked via OneToOneField
                attendance_date=datetime.now().date(),
                time_in=datetime.now(),
                image=data
            )
            attendance.save()
            messages.success(request, 'You have successfully checked in.')
            return redirect('attendance_list')

    return render(request, 'hrms/attendance_form.html')


@login_required
def attendance_check_out(request):
    try:
        attendance = Attendance.objects.filter(employee=request.user.employee, time_out__isnull=True).latest('time_in')
        attendance.time_out = datetime.now()
        attendance.save()
        messages.success(request, 'You have successfully checked out.')
    except Attendance.DoesNotExist:
        messages.error(request, 'No check-in record found for today.')
    return redirect('home')


@login_required
def attendance_detail(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    return render(request, 'hrms/attendance_detail.html', {'attendance': attendance})


@login_required
def attendance_update(request, attendance_id):
    attendance = get_object_or_404(Attendance, pk=attendance_id)
    if request.method == "POST":
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('attendance_list')
    else:
        form = AttendanceForm(instance=attendance)
    return render(request, 'hrms/attendance_update.html', {'form': form})


# Leave Views
@login_required
def leave_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'leave_start_date')
    order = request.GET.get('order', 'asc')

    logged_in_employee = get_object_or_404(Employee, user=request.user)
    employee_leaves = Leave.objects.filter(employee=logged_in_employee)

    leave_balance, created = LeaveBalance.objects.get_or_create(employee=logged_in_employee)

    leaves = Leave.objects.all()

    if query:
        leaves = leaves.filter(
            Q(employee__first_name__icontains=query) |
            Q(employee__last_name__icontains=query) |
            Q(leave_start_date__icontains=query) |
            Q(leave_end_date__icontains=query) |
            Q(leave_status__icontains=query)
        )

    if order == 'desc':
        sort_by = f'-{sort_by}'
    leaves = leaves.order_by(sort_by)

    context = {
        'leaves': leaves,
        'employee_leaves': employee_leaves,
        'leave_balance': leave_balance,
        'query': query,
        'sort_by': sort_by,
        'order': order
    }

    return render(request, 'hrms/leave_list.html', context)


@login_required
def add_leave(request):
    logged_in_employee = get_object_or_404(Employee, user=request.user)
    leave_balance, created = LeaveBalance.objects.get_or_create(employee=logged_in_employee)

    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        form = LeaveAddForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = logged_in_employee
            leave_days = (leave.leave_end_date - leave.leave_start_date).days + 1

            if leave_days <= 0:
                form.add_error(None, 'End date must be after start date.')
            else:
                if leave.leave_type == 'Annual':
                    if leave_days > leave_balance.annual_leave_balance:
                        form.add_error(None, 'Not enough annual leave balance.')
                    else:
                        leave_balance.annual_leave_balance -= leave_days
                        leave_balance.save()
                        leave.save()
                        print("Annual leave balance updated:", leave_balance.annual_leave_balance)
                        return redirect('leave_list')

                elif leave.leave_type == 'Medical':
                    if leave_days > leave_balance.medical_leave_balance:
                        form.add_error(None, 'Not enough medical leave balance.')
                    else:
                        leave_balance.medical_leave_balance -= leave_days
                        leave_balance.save()
                        leave.save()
                        print("Medical leave balance updated:", leave_balance.medical_leave_balance)
                        return redirect('leave_list')
        else:
            print("Form is not valid")
            print(form.errors)
    else:
        form = LeaveAddForm()

    return render(request, 'hrms/leave_add.html', {'form': form})


@login_required
@department_required('Human Resource')
def edit_leave_status(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.method == 'POST':
        form = LeaveStatusUpdateForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_list', leave_id=leave.id)  # Replace 'leave_detail' with your actual URL name
    else:
        form = LeaveStatusUpdateForm(instance=leave)
    return render(request, 'hrms/leave_edit.html', {'form': form})


@login_required
def leave_delete(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    leave.delete()
    return redirect('leave_list')


# Payroll Views
@department_required('Human Resource')
def payroll_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'employee__first_name')
    order = request.GET.get('order', 'asc')
    payrolls = search_and_filter_payrolls(query, sort_by, order)
    return render(request, 'hrms/payroll_list.html',
                  {'payrolls': payrolls, 'query': query, 'sort_by': sort_by, 'order': order})


@department_required('Human Resource')
def payroll_create(request):
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'hrms/payroll_form.html', {'form': form})


@department_required('Human Resource')
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


@department_required('Human Resource')
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

    return render(request, 'finance/create_sales.html', {'sales_form': sales_form, 'formset': formset})


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
