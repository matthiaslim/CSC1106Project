import base64

from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from ..crud_ops import search_and_filter_attendances, search_and_filter_departments, search_and_filter_employees, search_and_filter_payrolls
from ..forms import AttendanceForm, DepartmentForm, EmployeeForm, LeaveAddForm, LeaveStatusUpdateForm, PayrollForm, CustomUserCreationForm
from ..models.attendance import Attendance
from ..models.department import Department
from ..models.employee import Employee
from ..models.leave import Leave
from ..models.leaveBalance import LeaveBalance
from ..models.payroll import Payroll
from ..decorators import department_required
from datetime import datetime
from django.db.models import Q



# Employee Views
# @department_required('Human Resource')
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


# @department_required('Human Resource')
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'hrms/employee_detail.html', {'employee': employee})


# @department_required('Human Resource')
def employee_create(request):
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        user_form = CustomUserCreationForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            try:
                user = user_form.save()
                
                employee = form.save(commit=False)
                employee.user = user
                employee.save()
                
                return redirect('employee_list')
            except IntegrityError:
                form.add_error(None, "An employee with this user already exists.")
            
    else:
        user_form = CustomUserCreationForm()
        form = EmployeeForm()

    return render(request, 'hrms/employee_form.html', {'form': form, 'user_form' : user_form})


# @department_required('Human Resource')
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
# @department_required('Human Resource')
def department_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'department_name')
    order = request.GET.get('order', 'asc')
    departments = search_and_filter_departments(query, sort_by, order)
    return render(request, 'hrms/department_list.html',
                  {'departments': departments, 'query': query, 'sort_by': sort_by, 'order': order})


# @department_required('Human Resource')
def department_detail(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    return render(request, 'hrms/department_detail.html', {'department': department})


# @department_required('Human Resource')
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hrms/department_form.html', {'form': form})


# @department_required('Human Resource')
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


# @department_required('Human Resource')
def department_delete(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')


# Attendance Views
@login_required
def attendance_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'attendance_id')
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
# @department_required('Human Resource')
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
# @department_required('Human Resource')
def payroll_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'employee__first_name')
    order = request.GET.get('order', 'asc')
    payrolls = search_and_filter_payrolls(query, sort_by, order)
    return render(request, 'hrms/payroll_list.html',
                  {'payrolls': payrolls, 'query': query, 'sort_by': sort_by, 'order': order})


# @department_required('Human Resource')
def payroll_create(request):
    if request.method == "POST":
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'hrms/payroll_form.html', {'form': form})


# @department_required('Human Resource')
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


# @department_required('Human Resource')
def payroll_delete(request, payroll_id):
    payroll = get_object_or_404(Payroll, pk=payroll_id)
    payroll.delete()
    return redirect('payroll_list')

