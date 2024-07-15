import os
import pandas as pd
from django.core.management.base import BaseCommand
from csc1106app.models.product import Product
from csc1106app.models.department import Department

class Command(BaseCommand):
    help = 'Import products data from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'modified.csv'  # Update with your actual CSV file path
        df = pd.read_csv(file_path)

        # Insert data into the database
        for _, row in df.iterrows():
            product_exists = Product.objects.filter(product_name=row['name']).exists()
            if not product_exists:
                Product.objects.create(
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
                self.stdout.write(self.style.SUCCESS(f'Product {row["name"]} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Product {row["name"]} already exists'))

        departments_avail = ['Chairman', 'Human Resource', 'Finance', 'Customer Relation', 'Logistics']
        for i in departments_avail:
            department_exists = Department.objects.filter(department_name=i).exists()
            if not department_exists:
                Department.objects.create(
                    department_name=i
                )
                self.stdout.write(self.style.SUCCESS(f'Department {i} created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Department {i} already exists'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
