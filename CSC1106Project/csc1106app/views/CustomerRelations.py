from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..forms import CreateCustomerForm
from ..models.membership import Membership
from ..crud_ops import *
from ..decorators import department_required
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Customer Views
@login_required
# @department_required('Customer Relations')
def customer_management(request):
    memberships = Membership.objects.all()
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]
    data = {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'memberships': memberships}
    return render(request, 'customer/customer_management.html', data)


@login_required
# @department_required('Customer Relations')
def customer_details(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
    except Membership.DoesNotExist:
        # Handle the case where the customer does not exist
        membership = None

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                   {'title': f'Customer Details - {membership}'}]
    data = {'breadcrumbs': breadcrumbs, 'page_title': 'Customers', 'membership': membership}

    return render(request, 'customer/customer_details.html', data)


@login_required
# @department_required('Customer Relations')
def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            country = form.cleaned_data.get('country')
            membership_status = form.cleaned_data.get('membership_status')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')
            # call a func to save the data

            # m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address, phone_number=phone_number, dob=dob, country=country, status=status, age=age, address=address)
            # m1.save()
            expiry_date = datetime.now() + relativedelta(years=1)
            m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address,
                            phone_number=phone_number, points_expiry_date=expiry_date, member_expiry_date=expiry_date,
                            membership_status=membership_status, points=0, membership_level="Bronze", address=address,
                            country=country, date_of_birth=date_of_birth, gender=gender)
            m1.save()
            return redirect('customer_management')
    else:
        form = CreateCustomerForm()

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer', 'form': form})


@login_required
def update_customer(request, customerID):
    membership = Membership.objects.get(member_id=customerID)

    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():
            membership.first_name = form.cleaned_data.get('first_name')
            membership.last_name = form.cleaned_data.get('last_name')
            membership.email_address = form.cleaned_data.get('email_address')
            membership.phone_number = form.cleaned_data.get('phone_number')
            membership.date_of_birth = form.cleaned_data.get('date_of_birth')
            membership.country = form.cleaned_data.get('country')
            membership.membership_status = form.cleaned_data.get('membership_status')
            membership.gender = form.cleaned_data.get('gender')
            membership.address = form.cleaned_data.get('address')
            membership.save()

            return redirect('customer_management')
    else:

        form = CreateCustomerForm(instance=membership)

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/update_customer.html',
                  {'breadcrumbs': breadcrumbs, 'page_title': 'Create Customer', 'form': form})


@login_required
def delete_customer(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
        membership.delete()
    except Membership.DoesNotExist:
        # Handle the case where the customer does not exist
        membership = None

    return redirect('customer_management')

