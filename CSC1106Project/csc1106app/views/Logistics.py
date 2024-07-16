from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from ..forms import ProductForm, editProductForm, addOrderForm, editOrderForm
from ..models.product import Product
from ..models.stockOrder import StockOrder
from ..crud_ops import *
from ..decorators import department_required
import json

# Inventory Views
@login_required
@department_required('Logistics')
def inventory_management(request):
    # Fetch all products initially
    products = Product.objects.all()

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
        if form.is_valid:
            form.save()

            return redirect('inventory_management')
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
        order = editProductForm(request.POST,request.FILES,instance=product)
        
        order.save()
    return JsonResponse({'status' : 200, 'message' : 'updated product successfully'})


@login_required
@department_required('Logistics')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    try:
        if request.method == 'DELETE':
            product.delete()
        return JsonResponse({'status': 200, 'message': 'Product deleted successfully.'})
    except:
        return JsonResponse({'status': 400, 'message': 'Bad request.'})
    

@login_required
@department_required('Logistics')
def order_management(request):
    # Fetch all orders initially
    orders = StockOrder.objects.all()
    form = addOrderForm()
    editform = editOrderForm()

    return render(request, 'inventory/order_management.html', {'orders': orders, 'form': form , 'editform' : editform})

@login_required
@department_required('Logistics')
def create_order(request):
    if request.method == 'POST':
        form = addOrderForm(request.POST)
        # Perform validation
        if form.is_valid():
            form.save()
            return JsonResponse({"status": 200, "message": "Order has been successfully placed."})
        else:
            print(form.errors)
            return JsonResponse({"status": 400, "message": "Order creation failed."})
 
@login_required
@department_required('Logistics')
def edit_order(request,pk):
    if request.method == 'POST':
        stockOrder = get_object_or_404(StockOrder, pk=pk)
        form = editOrderForm(request.POST,instance=stockOrder)
        if form.is_valid():
            if request.POST.get('order_status') == 'Received':
                product = get_object_or_404(Product, pk=stockOrder.product.product_id)
                product.product_quantity += stockOrder.order_quantity
                product.save()

            form.save()
            return JsonResponse({"status": 200, "message": "Order has been successfully updated."})
        else:
            print(form.errors)
            return JsonResponse({"status": 400, "message": "Order creation failed."})