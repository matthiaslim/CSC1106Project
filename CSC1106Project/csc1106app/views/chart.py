from ..models import *
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime
from collections import defaultdict

def display_chart_information(request):
    current_year = datetime.now().year

    transactionProductItem = TransactionProduct.objects.filter(transaction_id__transaction_date__year=current_year)
    month = []
    data = []
    monthly_sums = defaultdict(float)

    for item in transactionProductItem:
        transaction_date = item.transaction_id.transaction_date
        
 
        month_year = transaction_date.strftime("%m")
        month_year = datetime.strptime(month_year,"%m").strftime("%B")
   
        monthly_sums[month_year] += item.transaction_price_per_unit


    for month_year, total_price in monthly_sums.items():
        month.append(month_year)
        data.append(total_price)
    
    return JsonResponse({'month':month, 'data':data})

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
    
    pendingInvoiceCount = {'total_quantity':0} if list(pendingInvoiceCount.values())[0] is None else pendingInvoiceCount

    return JsonResponse({"currentstock": totalProductQuantity , "pendingstock" : pendingInvoiceCount})

def top_selling_items(request):
    transcationItemLists = TransactionProduct.objects.all()
    transactionItemList = transcationItemLists.values('product_id').annotate(count = Sum('transaction_quantity')).order_by('-count')[:5]
    top_product_ids = [item['product_id'] for item in transactionItemList]
    
    product = Product.objects.filter(product_id__in=top_product_ids).values()


    return JsonResponse({"Product": list(product)})
