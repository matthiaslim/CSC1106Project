from django.db import models
from .product import Product

class StockOrder(models.Model):
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received')
    ]
    
    order_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_status = models.CharField(max_length=10,choices=STATUS_CHOICES,default="Pending")

    def __str__(self):
        return f'Quantity Value is {self.order_quantity}'
