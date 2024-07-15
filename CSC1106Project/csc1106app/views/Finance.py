from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import InvoiceForm, InvoiceProductFormSet, SalesForm, SalesProductFormSet
from ..models.product import Product
from ..crud_ops import *
from ..decorators import department_required


# Finance Views
def sales_management(request):
    return render(request, 'finance/sales_management.html')


def create_sales(request):
    if request.method == 'POST':
        sales_form = SalesForm(request.POST)
        formset = SalesProductFormSet(request.POST, request.FILES)
        print(formset.errors)
        if sales_form.is_valid() and formset.is_valid():
            sales = sales_form.save()
            formset.instance = sales
            formset.save()
            return redirect('sales_management')
    else:
        sales_form = SalesForm()
        formset = SalesProductFormSet()

    for form in formset.forms:
        form.set_initial_price()

    return render(request, 'finance/create_sales.html', {'sales_form': sales_form, 'formset': formset})


def invoice_management(request):
    return render(request, 'finance/invoice_management.html')


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


def get_product_price(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.product_sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
