from django.db import models
from .product import Product
from .invoice import Invoice


class InvoiceProduct(models.Model):
    invoice_product_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_quantity = models.IntegerField()
    invoice_price_per_unit = models.FloatField()
    payment_terms = models.CharField(max_length=30)