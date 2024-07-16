import django_filters
from .models import Invoice

class InvoiceFilter(django_filters.FilterSet): 
    # invoice_total_value_min = django_filters.NumberFilter(method='filter_invoice_total_value_min', label='Min Invoice Value')
    # invoice_total_value_max = django_filters.NumberFilter(method='filter_invoice_total_value_max', label='Max Invoice Value')

    class Meta:
        model = Invoice
        fields = {
            'invoice_date': ['gt', 'lt'],
            'payment_due_date': ['gt', 'lt'],
            'payment_terms': ['exact'], 
            'status': ['exact'], 
            'employee_id': ['exact']
        }
        # filter_overrides = {
        #     models.CharField: {
        #         'filter_class': django_filters.CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        #     models.DateField: {
        #         'filter_class': django_filters.BooleanFilter,
        #         'extra': lambda f: {
        #             'widget': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        #         },
        #     },
        # }
    
    # @classmethod
    # def filter_for_lookup(cls, f, lookup_type):
    #     # override date range lookups
    #     if isinstance(f, models.DateField) and lookup_type == 'range':
    #         return django_filters.DateRangeFilter, {}

    #     # use default behavior otherwise
    #     return super().filter_for_lookup(f, lookup_type)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['employee_id'].widget.attrs.update({'class': 'form-select'})

        # fields = {
        #     'invoice_date': ['gt', 'lt'],
            # 'payment_due_date': ['gt', 'lt'],
            # 'payment_terms': ['exact'],
            # 'status': ['exact'],
            # Assuming 'employee_id' filtering requires a dropdown of all employees
            # queryset=Employee.objects.all(), label="Employee", to_field_name="employee_id"
        # }

    # def filter_invoice_total_value_min(self, queryset, name, value):
    #     # Filter invoices having total_value >= value
    #     return queryset.annotate(
    #         invoice_total_value=Sum(F('invoiceproduct_set__invoice_quantity') * F('invoiceproduct_set__invoice_price_per_unit'))
    #     ).filter(total_value__gte=value)

    # def filter_invoice_total_value_max(self, queryset, name, value):
    #     # Filter invoices having total_value <= value
    #     return queryset.annotate(
    #         invoice_total_value=Sum(F('invoiceproduct_set__invoice_quantity') * F('invoiceproduct_set__invoice_price_per_unit'))
    #     ).filter(total_value__lte=value)