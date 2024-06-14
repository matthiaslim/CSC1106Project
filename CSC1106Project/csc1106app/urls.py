"""
URL configuration for CSC1106Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', login_required(views.index), name="home"),
    path('login', views.login_user, name="login"),
    path('register', views.register_user, name="register"),

    path('inventory/management', login_required(views.inventory_management), name="inventory_management"),
    path('inventory/statistics', login_required(views.inventory_statistics), name="inventory_statistics"),

    # Customer URLs
    path('customer/management', login_required(views.customer_management), name="customer_management"),
    path('customer/details/<int:customerID>', login_required(views.customer_details), name="customer_details"),
    path('customer/create', login_required(views.create_customer), name="create_customer")
]
