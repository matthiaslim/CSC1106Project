from ..models import *
from ..crud_ops import *
from django.http import JsonResponse
from django.db.models import Sum

def display_chart_information(request):
    return JsonResponse()

def get_product_details(request):
    ProductItems = Product.objects.all()
    lowStockItem = ProductItems.filter(product_quantity__lte=30).count()
    itemCategories = ProductItems.values('product_category').distinct().count()
    allItem = ProductItems.count()

    return JsonResponse({"lowstock": lowStockItem, "itemcategories": itemCategories, "allitem": allItem})

def inventory_summary(request):
    totalProductQuantity = Product.objects.aggregate(total_quantity=Sum('product_quantity'))

    pendingInvoiceItem = Invoice.objects.filter(status__in=["Pending","Completed"]).all()
    pendingInvoiceIds = pendingInvoiceItem.values_list('invoice_id',flat=True)
    pendingInvoiceCount = InvoiceProduct.objects.filter(invoice_id__in=pendingInvoiceIds).aggregate(total_quantity=Sum('invoice_quantity'))
    

    return JsonResponse({"currentstock": totalProductQuantity , "pendingstock" : pendingInvoiceCount})

def top_selling_items(request):
    return JsonResponse()
