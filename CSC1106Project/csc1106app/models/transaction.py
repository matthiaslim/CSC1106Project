from django.db import models
from .employee import Employee
from .membership import Membership

class Transaction(models.Model):
    PAYMENT_CHOICES = [
        ('Card', 'Card'),
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque')
    ]

    transaction_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    points_earned = models.IntegerField()
    transaction_date = models.DateField()
    payment_terms = models.CharField(max_length=30, choices=PAYMENT_CHOICES, default='Card')

    def __str__(self):
        return str(self.transaction_id)
