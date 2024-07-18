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
    #path('get_chart_information',login_required(views.get_chart_information), name="get_chart_information")

    # Inventory URLs
    path('inventory/management', login_required(views.inventory_management), name="inventory_management"),
    path('inventory/management/create', login_required(views.add_product), name="add_product"),
    path('inventory/get/<int:pk>', login_required(views.get_product), name="get_product"),
    path('inventory/update/<int:pk>', login_required(views.update_product), name='update_product'),
    path('inventory/delete/<int:pk>', login_required(views.delete_product), name='delete_product'),
    path('inventory/order_management',login_required(views.order_management), name="order_management"),
    path('inventory/order_management/edit/<int:pk>', login_required(views.edit_order), name="edit_order"),

    # Customer URLs
    path('customer/management', login_required(views.customer_management), name="customer_management"),
    path('customer/details/<int:customerID>', login_required(views.customer_details),
       name="customer_details"),
    path('customer/create', login_required(views.create_customer), name="create_customer"),
    path('customer/update/<int:customerID>', login_required(views.update_customer),
       name="update_customer"),
    path('customer/delete/<int:customerID>', login_required(views.delete_customer),
       name="delete_customer"),
    path('customer/order/<int:sales_id>/', views.sales_details, name="customer_order"),

    # Finance URLs
    path('finance/sales', views.sales_management, name="sales_management"),
    path('finance/sales/<int:sales_id>/', views.sales_details, name="sales_details"),
    path('finance/sales/create', views.create_sales, name="create_sales"),
    path('finance/sales/delete/<int:sales_id>', views.delete_sales, name='delete_sales'),
    path('finance/orders', views.invoice_management, name="invoice_management"),
    path('finance/orders/create', views.create_invoice, name="create_invoice"),
    path('finance/orders/<int:invoice_id>', views.invoice_details, name="invoice_details"),
    path('finance/update/<int:invoice_id>', views.update_invoice, name="update_invoice"),
    path('finance/orders/delete/<int:invoice_id>', views.delete_invoice, name='delete_invoice'),
    path('get-product-price/<int:product_id>/', views.get_product_price, name='get-product-price'),
    path('finance/financial_report', views.financial_report, name='financial_report'),

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
    path('generate_payroll/', views.generate_payroll, name='generate_payroll'),
    path('edit_payroll_bonus/<int:payroll_id>/', views.edit_payroll_bonus, name='edit_payroll_bonus'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
