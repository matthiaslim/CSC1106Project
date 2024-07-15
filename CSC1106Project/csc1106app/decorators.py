# decorators.py
from functools import wraps
from datetime import date, datetime
from django.shortcuts import render, get_object_or_404
from .models import Employee
from .models import Attendance


def department_required(*department_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            employee = Employee.objects.filter(user=request.user).first()
            if employee.department.department_name == 'Chairman' or employee.department.department_name in department_names:
                return view_func(request, *args, **kwargs)
            return render(request, 'base.html', {'permission_denied': True})

        return _wrapped_view

    return decorator


def user_check_in_status(request):
    is_checked_in = False
    is_checked_out = False

    if request.user.is_authenticated:
        user = request.user.id

        employee = Employee.objects.filter(user=user).first()
        today = date.today()

        if (employee is not None):
            employee_id = employee.employee_id
            userExists = Attendance.objects.filter(employee_id=employee_id, time_in__date=today).exists()
            userClockIn = Attendance.objects.filter(employee_id=employee_id, time_in__date=today).first()
            if (userExists):
                if (userClockIn != None):
                    is_checked_in = True

                if (userClockIn.time_out is not None):
                    if (userClockIn.time_out.date() == today):
                        is_checked_out = True

        return {'is_checked_in': is_checked_in, 'is_checked_out': is_checked_out, 'user_data': employee}

    return {'is_checked_in': is_checked_in, 'is_checked_out': is_checked_out}