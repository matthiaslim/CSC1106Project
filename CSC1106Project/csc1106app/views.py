from django.shortcuts import render

# Create your views here.


# Home View
def index(request):
    return render(request, 'index.html')

# Login View
def login(request):
    return render(request, 'login.html')

# Inventory Views
def inventory_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Management', 'url': '/inventory/management/'}]
    return render(request, 'inventory_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory'})


def inventory_statistics(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Statistics', 'url': '/inventory/statistics/'}]
    return render(request, 'inventory_statistics.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory Statistics'})

# Customer Views
def customer_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    return render(request, 'customer/customer_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Customers'})

def customer_details(request, customerID):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                    {'title': f'Customer Details - {customerID}'}]
    return render(request, 'customer/customer_details.html', {'breadcrumbs': breadcrumbs, 'page_title': f'Customer Details - {customerID}'})

def create_customer(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer'})