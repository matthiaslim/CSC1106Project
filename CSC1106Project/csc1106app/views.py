from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required


# Create your views here.


# Home View
def index(request):
    return render(request, 'index.html')


# Login View
def login_user(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a home page or another page after login
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to a home page or another page after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


# Inventory Views
@login_required
def inventory_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Management', 'url': '/inventory/management/'}]
    return render(request, 'inventory_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory'})


@login_required
def inventory_statistics(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Inventory'},
                   {'title': 'Statistics', 'url': '/inventory/statistics/'}]
    return render(request, 'inventory_statistics.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Inventory Statistics'})


# Customer Views
@login_required
def customer_management(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    return render(request, 'customer/customer_management.html', {'breadcrumbs': breadcrumbs, 'page_title': 'Customers'})


@login_required
def customer_details(request, customerID):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                   {'title': f'Customer Details - {customerID}'}]
    return render(request, 'customer/customer_details.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': f'Customer Details - {customerID}'})


@login_required
def create_customer(request):
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer'})
