from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import InvoiceForm, InvoiceProductFormSet, SalesForm, SalesProductFormSet
from ..filters import InvoiceFilter
from ..models.product import Product
from ..crud_ops import *
from ..decorators import department_required


# Finance Views
@login_required
# @department_required("Finance")
def sales_management(request):
    sales = Transaction.objects.all().prefetch_related('transactionproduct_set')
    for transaction in sales:
        transaction.total_value = sum(item.transaction_quantity * item.transaction_price_per_unit for item in transaction.transactionproduct_set.all())
    
    total_sum = sum(transaction.total_value for transaction in sales)
    total_transaction_count = len(sales)

    return render(request, 'finance/sales_management.html', {
        'sales': sales,
        'total_sum': total_sum,
        'total_invoice_count': total_transaction_count
    })

@login_required
# @department_required("Finance")
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
# @department_required("Finance")
def invoice_management(request):
    invoices = Invoice.objects.all().prefetch_related('invoiceproduct_set')

    for invoice in invoices:
        invoice.total_value = sum(item.invoice_quantity * item.invoice_price_per_unit for item in invoice.invoiceproduct_set.all())

    invoice_filter = InvoiceFilter(request.GET, queryset=invoices)  

    total_sum = sum(invoice.total_value for invoice in invoices)
    total_invoice_count = len(invoices)

    return render(request, 'finance/invoice_management.html', {
        'form': invoice_filter.form,
        'invoices': invoice_filter.qs,
        'total_sum': total_sum,
        'total_invoice_count': total_invoice_count
    }) 

@login_required
# @department_required("Finance")
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

@login_required
def get_product_price(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.product_sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
