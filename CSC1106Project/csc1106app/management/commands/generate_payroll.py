# payroll/management/commands/generate_payroll.py

from django.core.management.base import BaseCommand
from csc1106app.models import Payroll, Employee
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Generate payroll for all employees'

    def handle(self, *args, **kwargs):
        current_month = datetime.now().replace(day=1)
        start_date = current_month
        end_date = (current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        for employee in Employee.objects.all():
            hours_worked = employee.calculate_hours_worked(start_date, end_date)
            hourly_rate = employee.hourly_rate
            print(f"Employee: {employee.first_name} {employee.last_name}, Job Title: {employee.job_title}, Hourly Rate: {hourly_rate}")
            gross_salary = Decimal(hours_worked * hourly_rate)
            cpf_deduction = gross_salary * Decimal('0.17')
            bonus = Decimal('0.00')  
            net_salary = gross_salary - cpf_deduction + bonus

            # Debugging statements
            print(f"Hours Worked: {hours_worked}")
            print(f"Gross Salary: {gross_salary}")
            print(f"CPF Deduction: {cpf_deduction}")
            print(f"Bonus: {bonus}")
            print(f"Net Salary: {net_salary}")

            Payroll.objects.create(
                employee=employee,
                month=current_month,
                hours_worked=hours_worked,
                salary=gross_salary,
                cpf_deduction=cpf_deduction,
                bonus=bonus,
                net_pay=net_salary
            )
        self.stdout.write(self.style.SUCCESS('Payroll generated successfully'))
