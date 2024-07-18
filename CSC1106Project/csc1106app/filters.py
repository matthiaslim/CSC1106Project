import django_filters 
from django import forms
from django.db import models
from .models import Transaction, Invoice, Employee

class SalesFilter(django_filters.FilterSet): 
    class Meta:
        model = Transaction
        fields = {
            'transaction_date': ['gte', 'lte'],
            'payment_terms': ['exact'], 
            'employee_id': ['exact']
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                },
            },
        }

    payment_terms = django_filters.ChoiceFilter(choices=Invoice.PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    employee_id = django_filters.ModelChoiceFilter(queryset=Employee.objects.all(),widget=forms.Select(attrs={'class': 'form-select'}))


class InvoiceFilter(django_filters.FilterSet): 
    class Meta:
        model = Invoice
        fields = {
            'invoice_date': ['gte', 'lte'],
            'payment_due_date': ['gte', 'lte'],
            'payment_terms': ['exact'], 
            'status': ['exact'], 
            'employee_id': ['exact']
        }
        filter_overrides = {
            models.DateField: {
                'filter_class': django_filters.DateFilter,
                'extra': lambda f: {
                    'widget': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                },
            },
        }

    payment_terms = django_filters.ChoiceFilter(choices=Invoice.PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    status = django_filters.ChoiceFilter(choices=Invoice.STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    employee_id = django_filters.ModelChoiceFilter(queryset=Employee.objects.all(),widget=forms.Select(attrs={'class': 'form-select'}))

