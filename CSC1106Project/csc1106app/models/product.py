from django.db import models


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.CharField(max_length=255, blank=True)
    product_category = models.CharField(max_length=255)
    product_quantity = models.IntegerField()
    product_sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_location = models.CharField(max_length=50)
    product_width = models.IntegerField()
    product_height = models.IntegerField()
    product_length = models.IntegerField()
    product_image = models.ImageField(upload_to='product_image/', null=True, blank=True)

    def __str__(self):
        return f"{self.product_name}"
