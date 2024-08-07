# payroll/management/commands/generate_payroll.py

from django.core.management.base import BaseCommand
from csc1106app.models import Payroll, Employee
from datetime import  timedelta
from decimal import Decimal
from django.utils import timezone

class Command(BaseCommand):
    help = 'Generate payroll for all employees'

    def handle(self, *args, **kwargs):
        current_month = timezone.now().replace(day=1)

        # Check if payroll for the current month already exists
        if Payroll.objects.filter(month=current_month).exists():
            self.stdout.write(self.style.WARNING('Payroll for the current month has already been generated.'))
            return

        start_date = current_month
        end_date = (current_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        for employee in Employee.objects.all():
            hours_worked = employee.calculate_hours_worked(start_date, end_date)
            hourly_rate = employee.hourly_rate
            gross_salary = Decimal(hours_worked * hourly_rate)
            cpf_deduction = gross_salary * Decimal('0.17')
            bonus = Decimal('0.00')  # Set initial bonus to 0, HR can edit later
            net_salary = gross_salary - cpf_deduction + bonus

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
