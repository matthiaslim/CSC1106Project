from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import ProductForm, editProductForm
from ..crud_ops import *
from ..decorators import department_required

# Inventory Views
@login_required
@department_required('Logistics')
def inventory_management(request):
    # Fetch all products initially
    products = Product.objects.all().filter(is_deleted=0)

    # Handle filtering based on request parameters
    product_name = request.GET.get('product_name')
    product_category = request.GET.get('product_category')
    product_location = request.GET.get('product_location')

    if product_name:
        products = products.filter(product_name__icontains=product_name)
    if product_category:
        products = products.filter(product_category__icontains=product_category)
    if product_location:
        products = products.filter(product_location__icontains=product_location)

    form = editProductForm()

    return render(request, 'inventory/inventory_management.html', {'products': products , 'form': form })

@login_required
@department_required('Logistics')
def add_product(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Manage', 'url': '/inventory/management'},
                   {'title': 'Add Product', 'url': '/inventory/management/create'}, ]

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        filepath = request.FILES['product_image'] if 'product_image' in request.FILES else False

        if form.is_valid and filepath != False:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product successfully created.')
            return redirect('inventory_management')
        else:
            messages.error(request, 'Product is missing some fields.')
    else:
        form = ProductForm()
        
    return render(request, 'inventory/add_product.html', {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@department_required('Logistics')
def get_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    try:
        product_image_url = product.product_image.url if product.product_image else "/media/product_image/no_image.png"

        # Add or replace the product_image_url in the dictionary
        product_dict = {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'product_category': product.product_category,
            'product_quantity': product.product_quantity,
            'product_sale_price': product.product_sale_price,
            'product_location': product.product_location,
            'product_width': product.product_width,
            'product_height': product.product_height,
            'product_length': product.product_length,
            'product_image': product_image_url
        }

        return JsonResponse({'product': product_dict, 'status': 200})
    except Exception as e:
        return JsonResponse({'error': str(e), 'status': 500})


@login_required
@department_required('Logistics')
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = editProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid:
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Product has been updated successfully')
        else:
            return JsonResponse({"status":400,"message":form.errors})
        return JsonResponse({'status':200,"message":"succeeded successfully"})
    
    

@login_required
@department_required('Logistics')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        if request.method == 'DELETE':
            product.is_deleted = True
            product.save()
            messages.add_message(request, messages.SUCCESS, 'Product has been deleted successfully')
        return JsonResponse({'status': 200, 'message': 'Product deleted successfully.'})
    except:
        messages.add_message(request, messages.ERROR, 'Product has not been deleted!')
        return JsonResponse({'status': 400, 'message': 'Bad request.'})


@login_required
@department_required('Logistics')
def order_management(request):
    invoice = Invoice.objects.all()
    return render(request, 'inventory/order_management.html', {"invoices": invoice})
   
@login_required
@department_required('Logistics')
def edit_order(request,pk):

    invoices = InvoiceProduct.objects.filter(invoice_id=pk).all()
    
    if request.method == 'POST':

        invoice = get_object_or_404(Invoice,pk=pk)
        invoice.status = "Completed"
        invoice.save()

        for invoice in invoices:
            product = get_object_or_404(Product, pk=invoice.product_id.product_id)
            product.product_quantity += invoice.invoice_quantity
            
            product.save()

        messages.success(request, "Successfully imported product")
        return redirect('order_management')
    
    return render(request, 'inventory/edit_order.html',{"invoices":invoices, "invoice_id":pk})
  