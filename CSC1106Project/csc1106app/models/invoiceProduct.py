from django.db import models
from .product import Product
from .invoice import Invoice


class InvoiceProduct(models.Model):
    invoice_product_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_quantity = models.IntegerField()
    invoice_price_per_unit = models.FloatField()

    def sub_total(self):
        return self.invoice_quantity * self.invoice_price_per_unit

    def __str__(self):
        return str(self.invoice_id)