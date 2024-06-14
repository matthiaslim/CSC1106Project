import os
import pandas as pd
from django.core.management.base import BaseCommand

from csc1106app.models.product import Products

class Command(BaseCommand):
    help = 'Import products data from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'modified.csv'  # Update with your actual CSV file path
        df = pd.read_csv(file_path)

        # Insert data into the database
        for _, row in df.iterrows():
            Products.objects.create(
                product_name=row['name'],
                product_category=row['category'],
                product_sale_price=row['new_price'],
                product_location=row['product_location'],
                product_description=row['description'],
                product_length=row['Length'],
                product_height=row['height'],
                product_width=row['width'],
                product_quantity=row['quantity'],
            )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
