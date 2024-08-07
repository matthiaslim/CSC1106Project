import base64
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.management import call_command
from ..crud_ops import search_and_filter_attendances, search_and_filter_departments, search_and_filter_employees
from ..forms import  ( UserEditForm, AttendanceForm, DepartmentForm, 
                      EmployeeForm, LeaveAddForm, LeaveStatusUpdateForm, 
                      PayrollForm, CustomUserCreationForm)
from ..models import FailedLogin
from ..models.attendance import Attendance
from ..models.department import Department
from ..models.employee import Employee
from ..models.leave import Leave
from ..models.leaveBalance import LeaveBalance
from ..models.payroll import Payroll
from ..models.user import User
from ..decorators import department_required
from django.db.models import Q
from django.utils import timezone


# Employee Views
@login_required
@department_required('Human Resource')
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

@login_required
@department_required('Human Resource')
def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    user = get_object_or_404(User, pk=employee.user_id)
    return render(request, 'hrms/employee_detail.html', {'employee': employee, 'is_locked': user.is_locked})

@login_required
@department_required('Human Resource')
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
                
                messages.success(request, 'Employee created successfully.')
                return redirect('employee_list')
            except IntegrityError:
                form.add_error(None, "An employee with this user already exists.")
                messages.error(request, "An employee with this user already exists.")
        else:
            message = "";
            for field, errors in form.errors.items():
                for error in errors:
                    message += f"{error}\n"

            for field, errors in user_form.errors.items():
                for error in errors:
                    message += f"{error}\n"
                    
            messages.error(request, message, extra_tags='danger')

    else:
        user_form = CustomUserCreationForm()
        form = EmployeeForm()

    return render(request, 'hrms/employee_form.html', {'form': form, 'user_form' : user_form})

@login_required
@department_required('Human Resource')
def employee_unlock(request, employee_id):
    if request.method == "POST":
        employee = get_object_or_404(Employee, pk=employee_id)
        user = get_object_or_404(User, pk=employee.user_id)


        if user.is_locked:
            user.is_locked = False
            user.save()
            FailedLogin.objects.filter(user=user).delete()

            messages.success(request, "Account successfully unlocked")

            return redirect('employee_detail', employee_id=employee_id)

        elif not user.is_locked:
            messages.error(request, "Account is not locked", extra_tags='danger')
            return redirect('employee_detail', employee_id=employee_id)

    messages.error(request, "Failed to unlock account", extra_tags='danger')
    return redirect('employee_detail', employee_id=employee_id)


@login_required
@department_required('Human Resource')
def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    user = get_object_or_404(User, pk=employee.user_id)

    currentUserProfile = get_object_or_404(Employee, user_id=request.user)
    if employee.department.department_name == 'Chairman' and not currentUserProfile.department.department_name == "Chairman":
        return redirect("employee_list")
    
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        user_form = UserEditForm(request.POST, instance=user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Employee updated successfully.')
            return redirect('employee_list')
        else:
            messages.error(request, 'Employee Creation Failed.')
    else:
        user_form = UserEditForm(instance=user)
        form = EmployeeForm(instance=employee)
    return render(request, 'hrms/employee_form.html', {'form': form , 'user_form': user_form})


@login_required
@department_required('Human Resource')
def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == "POST":
        employee.delete()
        messages.success(request, 'Employee was deleted successfully.')
        return redirect('employee_list')


# Department Views
@login_required
@department_required('Human Resource')
def department_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'department_name')
    order = request.GET.get('order', 'asc')
    
    departments = search_and_filter_departments(query, sort_by, order).exclude(department_name='Chairman')

    departments = departments.prefetch_related('employees')

    return render(request, 'hrms/department_list.html', {
        'departments': departments,
        'query': query,
        'sort_by': sort_by,
        'order': order
    })

@login_required
@department_required('Human Resource')
def department_create(request):
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department created successfully.')
            return redirect('department_list')
        else:
            messages.error(request, 'Department creation failed.')
            return redirect('department_list')
    else:
        form = DepartmentForm()
    return render(request, 'hrms/department_form.html', {'form': form})


@login_required
@department_required('Human Resource')
def department_update(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department edited successfully.')
        else:
            messages.error(request, 'Departmnet update failed')
        return redirect('department_list')
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'hrms/department_form.html', {'form': form})


# Attendance Views
@login_required
@department_required('Human Resource')
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
                employee=employee, 
                time_in=timezone.now(),
                image=data
            )
            attendance.save()
            messages.success(request, 'You have successfully checked in.')
            return redirect('home')

    return render(request, 'hrms/attendance_form.html')


@login_required
def attendance_check_out(request):
    try:
        attendance = Attendance.objects.filter(employee=request.user.employee, time_out__isnull=True).latest('time_in')
        attendance.time_out = timezone.now()
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
            messages.success(request, 'Attendance updated successfully.')
            return redirect('attendance_list')
        else:
            messages.error(request, 'Error updating attendance.')
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
        form = LeaveAddForm(request.POST)
        if form.is_valid():
            leave_start_date = form.cleaned_data.get('leave_start_date')
            leave_end_date = form.cleaned_data.get('leave_end_date')
            leave_type = form.cleaned_data.get('leave_type')

            leave_days = (leave_end_date - leave_start_date).days + 1
            if leave_days <= 0:
                messages.error(request, 'End date must be after start date.')
            else:
                conflicting_leave = Leave.objects.filter(
                    employee=logged_in_employee,
                    leave_start_date__lte=leave_end_date,
                    leave_end_date__gte=leave_start_date
                ).exists()

                if conflicting_leave:
                    messages.error(request, 'You cannot have overlapping leaves on the same day.')
                else:
                    if leave_type == 'Annual' and leave_days > leave_balance.annual_leave_balance:
                        messages.error(request, 'Not enough annual leave balance.')
                    elif leave_type == 'Medical' and leave_days > leave_balance.medical_leave_balance:
                        messages.error(request, 'Not enough medical leave balance.')
                    else:
                        leave = form.save(commit=False)
                        leave.employee = logged_in_employee
                        leave.save()
                        
                        if leave_type == 'Annual':
                            leave_balance.annual_leave_balance -= leave_days
                        elif leave_type == 'Medical':
                            leave_balance.medical_leave_balance -= leave_days
                        leave_balance.save()

                        messages.success(request, 'Leave applied successfully.')
                        return redirect('leave_list')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        employeeData = request.user.employee
        initial_data = {
            "employee_name": f"{employeeData.first_name} {employeeData.last_name}",
            "employee_id": employeeData.employee_id
        }
        form = LeaveAddForm(initial=initial_data)

    return render(request, 'hrms/leave_add.html', {'form': form, 'leave_balance': leave_balance})

@login_required
@department_required('Human Resource')
def edit_leave_status(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.method == 'POST':
        form = LeaveStatusUpdateForm(request.POST, instance=leave)
        if form.is_valid():

            leave_status = request.POST.get('leave_status')
            if (leave_status == 'Denied'):
                leave_days = (leave.leave_end_date - leave.leave_start_date).days + 1

                # add back to the stuff 
                leaveBalanceObj = get_object_or_404(LeaveBalance, employee = leave.employee)
                
                dict_status = {
                    "Annual": "annual_leave_balance",
                    "Medical": "medical_leave_balance"
                }
                label_status = dict_status.get(leave.leave_type)

                if label_status: 
                    setattr(leaveBalanceObj, label_status, getattr(leaveBalanceObj, label_status) + leave_days)

                leaveBalanceObj.save()
                
            form.save()
            messages.success(request, 'Leave updated successfully.')
            return redirect('leave_list')
        else:
            messages.error(request, 'Error updating leave.')
            return redirect('leave_list')
    else:
        form = LeaveStatusUpdateForm(instance=leave)
    return render(request, 'hrms/leave_edit.html', {'form': form})

# Payroll Views
@login_required
def payroll_list(request):
    query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'employee__first_name')
    order = request.GET.get('order', 'asc')

    user_data = request.user.employee 

    if user_data.department.department_name in ['Human Resource', 'Chairman']:
        all_payrolls = Payroll.objects.all().order_by(sort_by if order == 'asc' else f'-{sort_by}')
        user_payrolls = Payroll.objects.filter(employee=user_data).order_by(sort_by if order == 'asc' else f'-{sort_by}')
    else:
        all_payrolls = None
        user_payrolls = Payroll.objects.filter(employee=user_data).order_by(sort_by if order == 'asc' else f'-{sort_by}')

    return render(request, 'hrms/payroll_list.html', {
        'all_payrolls': all_payrolls,
        'user_payrolls': user_payrolls,
        'query': query,
        'sort_by': sort_by,
        'order': order
    })

@login_required
@department_required('Human Resource')
def generate_payroll(request):
    current_month = timezone.now().replace(day=1)

    if Payroll.objects.filter(month=current_month).exists():
        messages.warning(request, 'Payroll for the current month has already been generated.')
        return redirect('payroll_list')
    
    call_command('generate_payroll')
    messages.success(request, 'Payroll generated successfully.')
    return redirect('payroll_list')

@login_required
@department_required('Human Resource')
def edit_payroll_bonus(request, payroll_id):
    payroll = get_object_or_404(Payroll, payroll_id=payroll_id)
    if request.method == 'POST':
        form = PayrollForm(request.POST, instance=payroll)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll updated successfully.')
            return redirect('payroll_list')
        else:
            messages.error(request, 'Error updating payroll.')
            return redirect('payroll_list')
    else:
        form = PayrollForm(instance=payroll)
    return render(request, 'hrms/payroll_form.html', {'form': form, 'payroll': payroll})