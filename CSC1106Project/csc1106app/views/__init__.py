from .chart import (get_chart_information)

from .authentication import (index,login_user,logout_user,settings, onboard)

from .Logistics import (inventory_management,add_product,get_product,update_product,delete_product,order_management,edit_order)

from .CustomerRelations import (customer_management,customer_details,create_customer,update_customer,delete_customer)

from .HumanResource import (employee_list,employee_detail,employee_create,employee_update,employee_delete,department_list,
                            department_detail,department_create,department_update,department_delete,attendance_list,
                            attendance_create,attendance_check_out,attendance_detail,attendance_update,leave_list,add_leave,
                            edit_leave_status,payroll_list,edit_payroll_bonus,generate_payroll)

from .Finance import (sales_management, create_sales, sales_details, delete_sales, invoice_management,
                      create_invoice, update_invoice, delete_invoice, get_product_price, financial_report,
                      invoice_details)


__all__ = [
    'get_chart_information',
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
    'employee_update',
    'employee_delete',
    'department_list',
    'department_detail',
    'department_create',
    'department_update',
    'department_delete',
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
    'delete_sales',
    'invoice_management',
    'invoice_details',
    'create_invoice',
    'get_product_price',
    'update_invoice',
    'delete_invoice',
    'financial_report'
]