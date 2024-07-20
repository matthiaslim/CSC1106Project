from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import os

from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from ..forms import InvoiceForm, InvoiceProductFormSet, SalesForm, SalesProductFormSet
from ..filters import InvoiceFilter, SalesFilter
from ..models.product import Product
from ..crud_ops import *
from ..decorators import department_required

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfbase.pdfmetrics import stringWidth

from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings

# Variables
current_year = date.today().year


# Finance Views
@login_required
@department_required("Finance")
def sales_management(request):
    sales = Transaction.objects.all().prefetch_related('transactionproduct_set')
    total_quantity_sold = 0

    for transaction in sales:
        transaction.total_value = sum(item.transaction_quantity * item.transaction_price_per_unit for item in
                                      transaction.transactionproduct_set.all())
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
# def create_sales(request):
#     if request.method == 'POST':
#         sales_form = SalesForm(request.POST)
#         formset = SalesProductFormSet(request.POST, request.FILES)
#         print(formset.errors)
#         if sales_form.is_valid() and formset.is_valid():
#             sales = sales_form.save()
#             point_earned = sales_form.cleaned_data.get('points_earned')
#             member = sales_form.cleaned_data.get('membership_id')
#             member.points += point_earned
#             formset.instance = sales
#             member.save()
#             formset.save()
#             pdf_buffer = generate_sales(sales)
#             return redirect('sales_management')
#     else:
#         sales_form = SalesForm()
#         formset = SalesProductFormSet()

#     for form in formset.forms:
#         form.set_initial_price()

#     return render(request, 'finance/create_sales.html', {'sales_form': sales_form, 'formset': formset})

def create_sales(request):
    if request.method == 'POST':
        sales_form = SalesForm(request.POST)
        formset = SalesProductFormSet(request.POST, request.FILES)
        print(formset.errors)
        if sales_form.is_valid() and formset.is_valid():
            # Start a transaction
            with transaction.atomic():
                # Check product quantities before proceeding
                all_products_sufficient = True
                for form in formset:
                    product_obj = form.cleaned_data.get('product_id')
                    sold_quantity = form.cleaned_data.get('transaction_quantity')
                    # Get product ID
                    if product_obj:
                        product_id = product_obj.product_id
                        product = Product.objects.get(product_id=product_id)

                    if product.product_quantity < sold_quantity:
                        all_products_sufficient = False
                        messages.error(request, f"Insufficient quantity for product {product.product_name}.")
                        break  # Exit loop if product has insufficient quantity
                
                if all_products_sufficient:
                    sales = sales_form.save()
                    point_earned = sales_form.cleaned_data.get('points_earned')
                    member = sales_form.cleaned_data.get('membership_id')
                    member.points += point_earned
                    member.save()
                    
                    # Update product quantities
                    for form in formset:
                        product_obj = form.cleaned_data.get('product_id')
                        sold_quantity = form.cleaned_data.get('transaction_quantity')
                        # Get product ID
                        if product_obj:
                            product_id = product_obj.product_id
                            product = Product.objects.get(product_id=product_id)
                        product.product_quantity -= sold_quantity
                        product.save()

                    formset.instance = sales
                    formset.save()
                    pdf_buffer = generate_sales(sales)
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
            total_price = salesProduct.transaction_quantity * salesProduct.transaction_price_per_unit
            salesProduct.total_price = total_price
            subtotal += total_price

        pdf_file_path = os.path.join('media', 'sales', f"sales_{sales.transaction_id}.pdf").replace('\\', '/')

        if not default_storage.exists(pdf_file_path):
            generate_sales(sales)

    except Transaction.DoesNotExist:
        sales = None

    data = {
        'sales': sales,
        'salesProducts': salesProducts,
        'subtotal': subtotal,
        'pdf_file_path': pdf_file_path.replace('media/', '/media/')
    }

    return render(request, 'finance/sales_details.html', data)


@login_required
@department_required("Finance")
def update_sales(request, sales_id):
    if request.method == "POST":
        Transaction.objects.filter(transaction_id=sales_id).update(
            payment_terms=request.POST.get('payment_terms'),
            transaction_date=request.POST.get('transaction_date')
        )
        return JsonResponse({'success': True})


@login_required
@department_required("Finance")
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
        invoice.total_value = sum(
            item.invoice_quantity * item.invoice_price_per_unit for item in invoice.invoiceproduct_set.all())

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
        payment_due_date__range=[today, today + timedelta(days=30)]
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
        'total_invoice_count': total_invoice_count,
        'sum_due_today': sum_due_today,
        'count_due_today': count_due_today,
        'sum_due_30_days': sum_due_30_days,
        'count_due_30_days': count_due_30_days,
        'sum_overdue': sum_overdue,
        'count_overdue': count_overdue
    })


@login_required
@department_required("Finance")
def invoice_details(request, invoice_id):
    try:
        invoice = Invoice.objects.get(invoice_id=invoice_id)
        invoiceProducts = invoice.invoiceproduct_set.all()
        subtotal = 0
        for invoiceProduct in invoiceProducts:
            total_price = invoiceProduct.invoice_quantity * invoiceProduct.invoice_price_per_unit
            invoiceProduct.total_price = total_price
            subtotal += total_price

        pdf_file_path = os.path.join('media', 'invoices', f"invoice_{invoice.invoice_id}.pdf").replace('\\', '/')
        print(pdf_file_path)

        if not default_storage.exists(pdf_file_path):
            generate_invoice(invoice)

    except Invoice.DoesNotExist:
        invoice = None

    data = {
        'invoice': invoice,
        'invoiceProducts': invoiceProducts,
        'subtotal': subtotal,
        'pdf_file_path': pdf_file_path.replace('media/', '/media/')  # Adjust path for template usage
    }

    return render(request, 'finance/invoice_details.html', data)


def send_sales_email(request, sales_id):
    if request.method == 'POST':
        try:
            sales = Transaction.objects.get(transaction_id=sales_id)
            pdf_file_path = os.path.join(settings.MEDIA_ROOT, 'sales', f'sales_{sales.transaction_id}.pdf')

            customer_email = sales.membership_id.email_address

            email = EmailMessage(
                subject='Your Sales Document',
                body='Please find attached the sales document.',
                from_email=settings.EMAIL_HOST_USER,
                to=[customer_email]  # Replace with the recipient's email address
            )
            email.attach_file(pdf_file_path)
            email.send()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


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

            pdf_buffer = generate_invoice(invoice)
            return redirect('invoice_management')
    else:
        invoice_form = InvoiceForm()
        formset = InvoiceProductFormSet()

    return render(request, 'finance/create_invoice.html', {'invoice_form': invoice_form, 'formset': formset})


@login_required
@department_required("Finance")
def update_invoice(request, invoice_id):
    if request.method == "POST":
        Invoice.objects.filter(invoice_id=invoice_id).update(status=request.POST.get('product_status'))
        return JsonResponse({'success': True})


@login_required
@department_required("Finance")
def delete_invoice(request, invoice_id):
    if request.method == 'POST':
        invoice = get_object_or_404(Invoice, pk=invoice_id)
        invoice.delete()
        return redirect('invoice_management')
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def get_product_price(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        return JsonResponse({'price': product.product_sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)


# @login_required
# @department_required("Finance")
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
        'net_profit': net_profit,
    }


@login_required
def financial_report(request):
    # Current year
    current_year_financial_data = financial_data_for_year(current_year)

    # Previous year
    previous_year = current_year - 1
    previous_year_financial_data = financial_data_for_year(previous_year)

    # Year-on-year % change
    yoy_change_total_sales = calculate_yoy_change(
        current_year_financial_data['total_sales'],
        previous_year_financial_data['total_sales']
    )
    yoy_change_total_purchases = calculate_yoy_change(
        current_year_financial_data['total_purchases'],
        previous_year_financial_data['total_purchases']
    )
    yoy_change_employee_wages = calculate_yoy_change(
        current_year_financial_data['total_employee_wages'],
        previous_year_financial_data['total_employee_wages']
    )
    yoy_change_net_profit = calculate_yoy_change(
        current_year_financial_data['net_profit'],
        previous_year_financial_data['net_profit']
    )

    inventory = Product.objects.all()
    
    inventory_value = sum(product.product_total_value() for product in inventory)
    total_assets = inventory_value

    return render(request, 'finance/financial_report.html', {
        'current_year': current_year,
        'previous_year': previous_year,
        'current_year_financial_data': current_year_financial_data,
        'previous_year_financial_data': previous_year_financial_data,
        'yoy_change_total_sales': yoy_change_total_sales,
        'yoy_change_total_purchases': yoy_change_total_purchases,
        'yoy_change_employee_wages': yoy_change_employee_wages,
        'yoy_change_net_profit': yoy_change_net_profit,
        'inventory_value': inventory_value,
        'total_assets': total_assets,
    })


def calculate_yoy_change(current_year_value, previous_year_value):
    if previous_year_value == 0:
        return None
    else:
        return round(((current_year_value - previous_year_value) / previous_year_value) * 100)


def split_text_to_fit(text, font_name, font_size, max_width):
    """
    Splits a given text into lines so that each line fits within the specified maximum width.
    """
    lines = []
    words = text.split()
    current_line = words.pop(0)

    for word in words:
        # Check if adding the next word exceeds the max width
        if stringWidth(f"{current_line} {word}", font_name, font_size) <= max_width:
            current_line += f" {word}"
        else:
            # If it does, add the current line to lines and start a new line with the word
            lines.append(current_line)
            current_line = word
    lines.append(current_line)  # Add the last line

    return lines


def generate_invoice(invoice):
    buffer = BytesIO()

    # Create a canvas object
    c = canvas.Canvas(buffer, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, 750, "INVOICE")

    # Company Information
    c.setFont("Helvetica", 12)
    c.drawString(30, 720, "IslandFurniture")
    c.drawString(30, 705, "Blk 123 Woodlands Ave 6")
    c.drawString(30, 690, "#01-52, Singapore 324123")
    c.drawString(30, 675, "Phone: +65 6456 7890")
    c.drawString(30, 660, "Email: islandFurniture@email.com")

    # Invoice Details
    c.drawString(475, 758, f"Invoice #: {invoice.invoice_id}")
    c.drawString(475, 743, f"Date: {invoice.invoice_date.strftime('%Y-%m-%d')}")

    c.drawString(30, 525, f"Payment Terms: {invoice.payment_terms}")

    # Table Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 510, "Description")
    c.drawString(400, 510, "Quantity")
    c.drawString(470, 510, "Price")
    c.drawString(540, 510, "Total")

    y = 490
    total_amount = 0
    font_name = "Helvetica"
    font_size = 12
    max_width = 350

    for item in invoice.invoiceproduct_set.all():
        product_name_lines = split_text_to_fit(item.product_id.product_name, font_name, font_size, max_width)
        for line in product_name_lines:
            c.setFont("Helvetica", 12)
            c.drawString(30, y, line)
            y -= 15  # Adjust line spacing for multiline product names
        c.drawString(400, y + 15, str(item.invoice_quantity))
        c.drawString(470, y + 15, f"${item.invoice_price_per_unit:.2f}")
        item_total = item.invoice_quantity * item.invoice_price_per_unit
        c.drawString(540, y + 15, f"${item_total:.2f}")
        total_amount += item_total
        y -= 20  # Move to the next item

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 10, "Total:")
    c.drawString(540, y - 10, f"${total_amount:.2f}")

    # Thank you note
    c.setFont("Helvetica", 12)
    c.drawString(30, y - 60, "Thank you for your business!")

    c.save()

    buffer.seek(0)

    file_path = os.path.join('invoices', f"invoice_{invoice.invoice_id}.pdf")

    if default_storage.exists(file_path):
        default_storage.delete(file_path)
    default_storage.save(file_path, buffer)

    return buffer


def generate_sales(sales):
    buffer = BytesIO()

    # Create a canvas object
    c = canvas.Canvas(buffer, pagesize=letter)

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(30, 750, "SALES")

    # Company Information
    c.setFont("Helvetica", 12)
    c.drawString(30, 720, "IslandFurniture")
    c.drawString(30, 705, "Blk 123 Woodlands Ave 6")
    c.drawString(30, 690, "#01-52, Singapore 324123")
    c.drawString(30, 675, "Phone: +65 6456 7890")
    c.drawString(30, 660, "Email: islandFurniture@email.com")

    # Customer Information
    c.drawString(30, 620, "Bill To:")
    c.drawString(30, 605, f"{sales.membership_id.first_name} {sales.membership_id.last_name}")
    c.drawString(30, 590, f"{sales.membership_id.address}")
    c.drawString(30, 575, f"Phone: {sales.membership_id.phone_number}")
    c.drawString(30, 560, f"Email: {sales.membership_id.email_address}")

    # Invoice Details
    c.drawString(475, 758, f"Sales #: {sales.transaction_id}")
    c.drawString(475, 743, f"Date: {sales.transaction_date.strftime('%Y-%m-%d')}")

    c.drawString(30, 525, f"Payment Terms: {sales.payment_terms}")

    # Table Header
    c.setFont("Helvetica-Bold", 12)
    c.drawString(30, 510, "Description")
    c.drawString(400, 510, "Quantity")
    c.drawString(470, 510, "Price")
    c.drawString(540, 510, "Total")

    y = 490
    total_amount = 0
    font_name = "Helvetica"
    font_size = 12
    max_width = 350

    for item in sales.transactionproduct_set.all():
        product_name_lines = split_text_to_fit(item.product_id.product_name, font_name, font_size, max_width)
        for line in product_name_lines:
            c.setFont("Helvetica", 12)
            c.drawString(30, y, line)
            y -= 15  # Adjust line spacing for multiline product names
        c.drawString(400, y + 15, str(item.transaction_quantity))
        c.drawString(470, y + 15, f"${item.transaction_price_per_unit:.2f}")
        item_total = item.transaction_quantity * item.transaction_price_per_unit
        c.drawString(540, y + 15, f"${item_total:.2f}")
        total_amount += item_total
        y -= 20  # Move to the next item

    # Total
    c.setFont("Helvetica-Bold", 12)
    c.drawString(400, y - 10, "Points Earned:")
    c.drawString(540, y - 10, f"{sales.points_earned}")
    c.drawString(400, y - 25, "Total:")
    c.drawString(540, y - 25, f"${total_amount:.2f}")

    # Thank you note
    c.setFont("Helvetica", 12)
    c.drawString(30, y - 70, "Thank you for your business!")

    c.save()

    buffer.seek(0)

    file_path = os.path.join('sales', f"sales_{sales.transaction_id}.pdf")

    if default_storage.exists(file_path):
        default_storage.delete(file_path)
    default_storage.save(file_path, buffer)

    return buffer
