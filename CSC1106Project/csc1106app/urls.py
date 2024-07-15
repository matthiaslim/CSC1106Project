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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_required(views.index), name="home"),
    path('login', views.login_user, name="login"),
    path('logout', login_required(views.logout_user), name="logout"),
    path('settings', login_required(views.settings), name="settings"),
    path('onboard', login_required(views.onboard), name="onboard"),

    # Inventory URLs
    path('inventory/management', login_required(views.inventory_management), name="inventory_management"),
    path('inventory/management/create', login_required(views.add_product), name="add_product"),
    path('inventory/get/<int:pk>/', login_required(views.get_product), name="get_product"),
    path('inventory/update/<int:pk>/', login_required(views.update_product), name='update_product'),
    path('inventory/delete/<int:pk>/', login_required(views.delete_product), name='delete_product'),

    # Customer URLs
    path('customer/management', login_required(views.customer_management), name="customer_management"),
    path('customer/details/<int:customerID>', login_required(views.customer_details),
       name="customer_details"),
    path('customer/create', login_required(views.create_customer), name="create_customer"),
    path('customer/update/<int:customerID>', login_required(views.update_customer),
       name="update_customer"),
    path('customer/delete/<int:customerID>', login_required(views.delete_customer),
       name="delete_customer"),

    # Finance URLs
    path('finance/sales', views.sales_management, name="sales_management"),
    path('finance/sales/create', views.create_sales, name="create_sales"),
    path('finance/orders', views.invoice_management, name="invoice_management"),
    path('finance/orders/create', views.create_invoice, name="create_invoice"),
    path('get-product-price/<int:product_id>/', views.get_product_price, name='get-product-price'),

    # Employee URLs
    path('hr/employees/', views.employee_list, name='employee_list'),
    path('hr/employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('hr/employees/create/', views.employee_create, name='employee_create'),
    path('hr/employees/<int:employee_id>/update/', views.employee_update, name='employee_update'),
    path('hr/employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),

    # Department URLs
    path('hr/departments/', views.department_list, name='department_list'),
    path('hr/departments/<int:department_id>/', views.department_detail, name='department_detail'),
    path('hr/departments/create/', views.department_create, name='department_create'),
    path('hr/departments/<int:department_id>/update/', views.department_update, name='department_update'),
    path('hr/departments/<int:department_id>/delete/', views.department_delete, name='department_delete'),

    # Attendance URLs
    path('hr/attendances/', views.attendance_list, name='attendance_list'),
    path('hr/attendances/create/', views.attendance_create, name='attendance_create'),
    path('hr/attendances/<int:attendance_id>/', views.attendance_detail, name='attendance_detail'),
    path('hr/attendances/<int:attendance_id>/update/', views.attendance_update, name='attendance_update'),
    path('hr/attendances/check-out/', views.attendance_check_out, name='attendance_check_out'),

    # Leave URLs
    path('hr/leaves/', views.leave_list, name='leave_list'),
    path('hr/leaves/create/', views.add_leave, name='leave_create'),
    path('hr/leaves/<int:leave_id>/update/', views.edit_leave_status, name='leave_update'),

    # Payroll URLs
    path('hr/payrolls/', views.payroll_list, name='payroll_list'),
    path('hr/payrolls/create/', views.payroll_create, name='payroll_create'),
    path('hr/payrolls/<int:payroll_id>/update/', views.payroll_update, name='payroll_update'),
    path('hr/payrolls/<int:payroll_id>/delete/', views.payroll_delete, name='payroll_delete'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
