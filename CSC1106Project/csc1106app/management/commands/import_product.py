import os
import pandas as pd
from django.core.management.base import BaseCommand
from csc1106app.models.product import Product
from csc1106app.models.department import Department

from csc1106app.models.user import User
from csc1106app.models.employee import Employee
from datetime import datetime


class Command(BaseCommand):
    help = 'Import products data from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'modified.csv'  # Update with your actual CSV file path
        df = pd.read_csv(file_path)
        count_product = 0
        count_product_exist = 0
        count_department = 0
        count_department_exist = 0

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
                count_product += 1
            else:
                count_product_exist += 1
                self.stdout.write(self.style.WARNING(f'Product {row["name"]} already exists'))

        departments_avail = ['Chairman', 'Human Resource', 'Finance', 'Customer Relation', 'Logistics']
        for i in departments_avail:
            department_exists = Department.objects.filter(department_name=i).exists()
            if not department_exists:
                Department.objects.create(
                    department_name=i
                )
                count_department += 1
            else:
                count_department_exist += 1
                self.stdout.write(self.style.WARNING(f'Department {i} already exists'))

        # Create a superuser
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'

        if not User.objects.filter(email=email).exists():
            superuser = User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {email} created successfully'))

            # Add a record to the Employee table referencing the superuser
            try:
                department = Department.objects.get(pk=1)
                Employee.objects.create(
                    user=superuser,
                    first_name='Admin',
                    last_name='User',
                    department=department,
                    job_title='Administrator',
                    gender='NA',
                    date_of_birth='1970-01-01',  # Example date
                    hire_date=datetime.today().strftime('%Y-%m-%d'),  # Example date
                    employee_role='Administrator',
                    onboarded=True  # Set onboarded to True for the superuser
                )
                self.stdout.write(self.style.SUCCESS('Employee record for superuser created successfully'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating employee record: {e}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {email} already exists'))


        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        self.stdout.write(self.style.SUCCESS(f'Total product added {count_product}, No. of products exist: {count_product_exist}'))
        self.stdout.write(self.style.SUCCESS(f'Total product added {count_department}, No. of products exist: {count_department_exist}'))
