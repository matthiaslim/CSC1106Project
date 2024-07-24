from django.core.management.base import BaseCommand
from csc1106app.models.department import Department

from csc1106app.models.user import User
from csc1106app.models.employee import Employee
from django.utils import timezone


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Create a superuser
        email = ['Isaiah Ang','Matthias Lim','JunLong Ng','Edwin Hew','CheeJian Chuah','Deston Seet','XiengHua Tan','ShunHao Teo']
        roles = [1,1,1,1,5,4,3,2]

        for i in range(len(email)):
            surname = email[i].split(' ')[1]
            name = email[i].split(' ')[0]
            email_addr = name.lower() + "@gmail.com"
            password = name.lower() + "@123"

            if not User.objects.filter(email=email_addr).exists():
                user = User.objects.create_superuser(email=email_addr, password=password) if roles[i] == 1 else User.objects.create_user(email=email_addr, password=password)
                # Add a record to the Employee table referencing the superuser
                department = Department.objects.get(pk=roles[i])
                job_title = "Chairman" if roles[i] == 1 else "Manager"

                try:
                    Employee.objects.create(
                        user=user,
                        first_name= name,
                        last_name=surname,
                        department=department,
                        job_title= job_title,
                        gender='Male',
                        date_of_birth='1970-01-01',  # Example date
                        hire_date=timezone.now().strftime('%Y-%m-%d'),  # Example date
                        employee_role= job_title ,
                        onboarded=True  # Set onboarded to True for the superuser
                    )
                    self.stdout.write(self.style.SUCCESS(f'Employee record for {name} created successfully'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error creating employee record: {e}'))
            else:
                self.stdout.write(self.style.WARNING(f'Superuser {email} already exists'))

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
