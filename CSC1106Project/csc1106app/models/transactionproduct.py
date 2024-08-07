from django.db import models
from .transaction import Transaction
from .product import Product

class TransactionProduct(models.Model):
    transaction_product_id = models.AutoField(primary_key=True)
    transaction_id = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    transaction_quantity = models.IntegerField()
    transaction_price_per_unit = models.FloatField()

    def sub_total(self):
        return self.transaction_quantity * self.transaction_price_per_unit


    