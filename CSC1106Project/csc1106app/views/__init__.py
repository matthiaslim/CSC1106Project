from .chart import (display_chart_information,get_product_details,inventory_summary,top_selling_items)

from .authentication import (index,login_user,logout_user,settings, onboard)

from .Logistics import (inventory_management,add_product,get_product,update_product,delete_product,order_management,edit_order)

from .CustomerRelations import (customer_management,customer_details,create_customer,update_customer,delete_customer)

from .HumanResource import (employee_list, employee_detail, employee_create, employee_update, employee_delete,
<<<<<<< HEAD
                            department_list,
                            department_create, department_update, attendance_list,
=======
                            department_list, department_create, department_update, attendance_list,
>>>>>>> 7e7f1f6acb1032d712ac60799506547548e7d36d
                            attendance_create, attendance_check_out, attendance_detail, attendance_update, leave_list,
                            add_leave,
                            edit_leave_status, payroll_list, edit_payroll_bonus, generate_payroll, employee_unlock)

from .Finance import (sales_management, create_sales, sales_details, delete_sales, invoice_management,
                      create_invoice, update_invoice, delete_invoice, get_product_price, financial_report,
                      invoice_details, update_sales, send_sales_email)


__all__ = [
    'display_chart_information',
    'get_product_details',
    'inventory_summary',
    'top_selling_items',
    'index',
    'login_user',
    'logout_user',
    'onboard',
    'settings',
    'inventory_management',
    'order_management',
    'edit_order',
    'add_product',
    'get_product',
    'update_product',
    'delete_product',
    'customer_management',
    'customer_details',
    'create_customer',
    'update_customer',
    'delete_customer',
    'employee_list',
    'employee_detail',
    'employee_create',
    'employee_unlock',
    'employee_update',
    'employee_delete',
    'department_list',
    'department_create',
    'department_update',
    'attendance_list',
    'attendance_create',
    'attendance_check_out',
    'attendance_detail',
    'attendance_update',
    'leave_list',
    'add_leave',
    'edit_leave_status',
    'payroll_list',
    'edit_payroll_bonus',
    'generate_payroll',
    'sales_management',
    'create_sales',
    'sales_details',
    'send_sales_email',
    'update_sales',
    'delete_sales',
    'invoice_management',
    'invoice_details',
    'create_invoice',
    'get_product_price',
    'update_invoice',
    'delete_invoice',
    'financial_report'
]