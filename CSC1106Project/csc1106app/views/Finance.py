from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import InvoiceForm, InvoiceProductFormSet, SalesForm, SalesProductFormSet
from ..filters import InvoiceFilter, SalesFilter
from ..models.product import Product
from ..crud_ops import *
from ..decorators import department_required

from datetime import date, timedelta
from decimal import Decimal

# Variables
current_year = date.today().year

# Finance Views
@login_required
@department_required("Finance")
def sales_management(request):
    sales = Transaction.objects.all().prefetch_related('transactionproduct_set')
    total_quantity_sold = 0


    for transaction in sales:
        transaction.total_value = sum(item.transaction_quantity * item.transaction_price_per_unit for item in transaction.transactionproduct_set.all())
        total_quantity_sold += sum(item.transaction_quantity for item in transaction.transactionproduct_set.all())

        for item in transaction.transactionproduct_set.all():
            item.sub_total = item.sub_total()
    
    total_sum = sum(transaction.total_value for transaction in sales)
    total_transaction_count = len(sales)

    sales_filter = SalesFilter(request.GET, queryset=sales)  

    return render(request, 'finance/sales_management.html', {
        'form': sales_filter.form,
        'sales': sales_filter.qs,
        'current_year': current_year,
        'total_sum': total_sum,
        'total_quantity_sold': total_quantity_sold,
        'total_transaction_count': total_transaction_count,
    })

@login_required
@department_required("Finance")
def create_sales(request):
    if request.method == 'POST':
        sales_form = SalesForm(request.POST)
        formset = SalesProductFormSet(request.POST, request.FILES)
        print(formset.errors)
        if sales_form.is_valid() and formset.is_valid():
            sales = sales_form.save()
            point_earned = sales_form.cleaned_data.get('points_earned')
            member = sales_form.cleaned_data.get('membership_id')
            member.points += point_earned
            formset.instance = sales
            member.save()
            formset.save()
            return redirect('sales_management')
    else:
        sales_form = SalesForm()
        formset = SalesProductFormSet()

    for form in formset.forms:
        form.set_initial_price()

    return render(request, 'finance/create_sales.html', {'sales_form': sales_form, 'formset': formset})

@login_required
@department_required("Finance")
def sales_details(request, sales_id):
    try:
        sales = Transaction.objects.get(transaction_id=sales_id)
        salesProducts = sales.transactionproduct_set.all()
        subtotal = 0
        for salesProduct in salesProducts:
            total_price = salesProduct.transaction_quantity* salesProduct.transaction_price_per_unit
            salesProduct.total_price = total_price
            subtotal += total_price

    except Transaction.DoesNotExist:
        sales = None

    data = {
        'sales': sales,
        'salesProducts': salesProducts,
        'subtotal': subtotal
    }

    return render(request, 'finance/sales_details.html', data)

# @login_required
def delete_sales(request, sales_id):
    if request.method == 'POST':
        sales = get_object_or_404(Transaction, transaction_id=sales_id)
        sales.delete()
        return redirect('sales_management')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
@department_required("Finance")
def invoice_management(request):
    invoices = Invoice.objects.all().prefetch_related('invoiceproduct_set')

    for invoice in invoices:
        invoice.total_value = sum(item.invoice_quantity * item.invoice_price_per_unit for item in invoice.invoiceproduct_set.all())

        for item in invoice.invoiceproduct_set.all():
            item.sub_total = item.sub_total()

    # Revenue yearly
    total_sum = sum(invoice.total_value for invoice in invoices)
    total_invoice_count = len(invoices)

    # Payment Dues 
    today = date.today()
    invoices_due_today = invoices.filter(payment_due_date=today)
    sum_due_today = sum(invoice.total_value() for invoice in invoices_due_today)   
    count_due_today = len(invoices_due_today)

    invoices_due_30_days = invoices.filter(
        payment_due_date__range=[today, today+timedelta(days=30)]
    )
    sum_due_30_days = sum(invoice.total_value() for invoice in invoices_due_30_days)
    count_due_30_days = len(invoices_due_30_days)

    overdue_invoices = invoices.filter(payment_due_date__lt=today)
    sum_overdue = sum(invoice.total_value() for invoice in overdue_invoices)
    count_overdue = len(overdue_invoices)

    invoice_filter = InvoiceFilter(request.GET, queryset=invoices)  

    return render(request, 'finance/invoice_management.html', {
        'form': invoice_filter.form,
        'invoices': invoice_filter.qs,
        'current_year': current_year,
        'total_sum': total_sum,
        'total_invoice_count': total_invoice_count
    }) 

@login_required
@department_required("Finance")
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

# @login_required
@department_required("Finance")
def update_invoice(request,invoice_id):
    if request.method == "POST":
        Invoice.objects.filter(invoice_id=invoice_id).update(status=request.POST.get('product_status'))
        return JsonResponse({'success': True})

# @login_required
def delete_invoice(request, pk):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=pk)
        invoice.delete()
        return redirect('invoice_management')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

# @login_required
def get_product_price(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.product_sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
def financial_data_for_year(year):
    sales = Transaction.objects.filter(transaction_date__year=year)
    purchases = Invoice.objects.filter(invoice_date__year=year)
    payroll = Payroll.objects.filter(month__year=year)

    total_sales = Decimal(sum(sale.total_value() for sale in sales))
    total_purchases = Decimal(sum(invoice.total_value() for invoice in purchases))
    total_employee_wages = Decimal(sum(item.net_pay for item in payroll))

    net_profit = total_sales - total_purchases - total_employee_wages

    return {
        'total_sales': total_sales,
        'total_purchases': total_purchases,
        'total_employee_wages': total_employee_wages,
        'net_profit': net_profit
    }

# @login_required
def financial_report(request):
    # Current year
    current_year_financial_data = financial_data_for_year(current_year)

    # Previous year
    previous_year = current_year - 1
    previous_year_financial_data = financial_data_for_year(previous_year)

    # Year-on-year % change
    try:
        yoy_change_total_sales = round(((current_year_financial_data['total_sales'] - 
                                   previous_year_financial_data['total_sales']) / 
                                   previous_year_financial_data['total_sales']) * 100)
        yoy_change_total_purchases = round(((current_year_financial_data['total_purchases'] - 
                                       previous_year_financial_data['total_purchases']) / 
                                       previous_year_financial_data['total_purchases']) * 100)
        yoy_change_employee_wages = round(((current_year_financial_data['total_employee_wages'] - 
                                      previous_year_financial_data['total_employee_wages']) / 
                                      previous_year_financial_data['total_employee_wages']) * 100)
        yoy_change_net_profit = round(((current_year_financial_data['net_profit'] -
                                  previous_year_financial_data['net_profit']) /
                                  previous_year_financial_data['net_profit']) * 100)
    except ZeroDivisionError:
        yoy_change_total_sales = 0
        yoy_change_total_purchases = 0
        yoy_change_employee_wages = 0
        yoy_change_net_profit = 0

    return render(request, 'finance/financial_report.html', {
        'current_year': current_year,
        'previous_year': previous_year, 
        'current_year_financial_data': current_year_financial_data,
        'previous_year_financial_data': previous_year_financial_data,
        'yoy_change_total_sales': yoy_change_total_sales,
        'yoy_change_total_purchases': yoy_change_total_purchases,
        'yoy_change_employee_wages': yoy_change_employee_wages,
        'yoy_change_net_profit': yoy_change_net_profit
    })