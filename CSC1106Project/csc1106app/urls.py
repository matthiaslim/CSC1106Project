"""
URL configuration for CSC1106Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name="home"),
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),

    path('inventory/management', login_required(views.inventory_management), name="inventory_management"),
    path('inventory/statistics', login_required(views.inventory_statistics), name="inventory_statistics"),

    # Customer URLs
    path('customer/management', login_required(views.customer_management), name="customer_management"),
    path('customer/details/<int:customerID>', login_required(views.customer_details), name="customer_details"),
    path('customer/create', login_required(views.create_customer), name="create_customer"),

    # Employee URLs
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),

    # Department URLs
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/<int:department_id>/update/', views.department_update, name='department_update'),
    path('departments/<int:department_id>/delete/', views.department_delete, name='department_delete'),

    # Attendance URLs
    path('attendances/', views.attendance_list, name='attendance_list'),
    path('attendances/create/', views.attendance_create, name='attendance_create'),
    path('attendances/<int:attendance_id>/update/', views.attendance_update, name='attendance_update'),
    path('attendances/<int:attendance_id>/delete/', views.attendance_delete, name='attendance_delete'),

    # Leave URLs
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/create/', views.leave_create, name='leave_create'),
    path('leaves/<int:leave_id>/update/', views.leave_update, name='leave_update'),
    path('leaves/<int:leave_id>/delete/', views.leave_delete, name='leave_delete'),

    # Payroll URLs
    path('payrolls/', views.payroll_list, name='payroll_list'),
    path('payrolls/create/', views.payroll_create, name='payroll_create'),
    path('payrolls/<int:payroll_id>/update/', views.payroll_update, name='payroll_update'),
    path('payrolls/<int:payroll_id>/delete/', views.payroll_delete, name='payroll_delete'),
]

