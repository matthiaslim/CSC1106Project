# decorators.py
from functools import wraps
from django.shortcuts import render
from .models import Employee


def department_required(*department_names):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            employee = Employee.objects.filter(user=request.user).first()
            if employee.department.department_name == 'Chairperson' or employee.department.department_name in department_names:
                return view_func(request, *args, **kwargs)
            return render(request, 'base.html', {'permission_denied': True})

        return _wrapped_view

    return decorator
