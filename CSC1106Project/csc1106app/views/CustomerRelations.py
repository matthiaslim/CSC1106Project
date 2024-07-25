from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms import CreateCustomerForm
from ..crud_ops import *
from ..decorators import department_required
from dateutil.relativedelta import relativedelta
from ..filters import MembershipFilter
from django.utils import timezone


# Customer Views
@login_required
@department_required('Customer Relation')
def customer_management(request):
    customer_filter = MembershipFilter(request.GET, queryset=Membership.objects.all())
    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'}]

    total_customers = Membership.objects.count()
    active_customers = Membership.objects.filter(membership_status="Active").count()
    inactive_customers = Membership.objects.exclude(membership_status="Active").count()

    data = {
        'breadcrumbs': breadcrumbs,
        'memberships': customer_filter.qs,
        'filter': customer_filter.form,
        'total_customers': total_customers,
        'active_customers': active_customers,
        'inactive_customers': inactive_customers
    }

    return render(request, 'customer/customer_management.html', data)


@login_required
@department_required('Customer Relation')
def customer_details(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
        member_sales = Transaction.objects.filter(membership_id_id=membership.member_id).select_related(
            'employee_id')
    except Membership.DoesNotExist:
        membership = None
    except Transaction.DoesNotExist:
        member_sales = None

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management/'},
                   {'title': f'Customer Details - {membership}'}]
    data = {'breadcrumbs': breadcrumbs, 'membership': membership,
            'member_sales': member_sales}

    return render(request, 'customer/customer_details.html', data)


@login_required
@department_required('Customer Relation')
def create_customer(request):
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST)
        if form.is_valid():

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email_address = form.cleaned_data.get('email_address')
            phone_number = form.cleaned_data.get('phone_number')
            date_of_birth = form.cleaned_data.get('date_of_birth')
            country = form.cleaned_data.get('country')
            membership_status = form.cleaned_data.get('membership_status')
            gender = form.cleaned_data.get('gender')
            address = form.cleaned_data.get('address')

            expiry_date = timezone.now() + relativedelta(years=1)
            m1 = Membership(first_name=first_name, last_name=last_name, email_address=email_address,
                            phone_number=phone_number, points_expiry_date=expiry_date, member_expiry_date=expiry_date,
                            membership_status=membership_status, points=0, membership_level="Bronze", address=address,
                            country=country, date_of_birth=date_of_birth, gender=gender)
            m1.save()
            messages.add_message(request, messages.SUCCESS, 'Customer Created Successfully.')
            return redirect('customer_management')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to create customer.')
            return redirect('customer_management')
    else:
        form = CreateCustomerForm()

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/create_customer.html',
                  {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@department_required('Customer Relation')
def update_customer(request, customerID):
    membership = Membership.objects.get(member_id=customerID)
    
    if request.method == 'POST':
        form = CreateCustomerForm(request.POST, instance=membership)
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
            messages.add_message(request, messages.SUCCESS, 'Customer Details Saved Successfully.')
            return redirect('customer_management')
        else:
            messages.add_message(request, messages.ERROR, 'Failed to save customer details.')
            return redirect('customer_management')
    else:

        form = CreateCustomerForm(instance=membership)

    breadcrumbs = [{'title': 'Home', 'url': '/'},
                   {'title': 'Customer'},
                   {'title': 'Management', 'url': '/customer/management'},
                   {'title': 'Create Customer'}]
    return render(request, 'customer/update_customer.html',
                  {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@department_required('Customer Relation')
def delete_customer(request, customerID):
    try:
        membership = Membership.objects.get(member_id=customerID)
        membership.delete()
        messages.add_message(request, messages.SUCCESS, 'Customer Deleted Successfully.')
    except Membership.DoesNotExist:
        membership = None
        messages.add_message(request, messages.ERROR, 'Customer does not exist.')
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Failed to delete customer.')

    return redirect('customer_management')
