from django.shortcuts import render

# Create your views here.


# Home View
def index(request):
    return render(request, 'index.html')


# Inventory Views
def inventory_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Management', 'url': '/inventory/management/'}]
    return render(request, 'inventory_management.html', {'breadcrumbs': breadcrumbs})


def inventory_statistics(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Statistics', 'url': '/inventory/statistics/'}]
    return render(request, 'inventory_statistics.html', {'breadcrumbs': breadcrumbs})
