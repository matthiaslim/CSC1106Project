from django.db import models

class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255)
    product_category = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_sale_price = models.FloatField()
    product_location = models.CharField(max_length=50)
    product_width = models.IntegerField()
    product_height = models.IntegerField()
    product_length = models.IntegerField()
