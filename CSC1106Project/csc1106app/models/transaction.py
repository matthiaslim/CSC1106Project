from django.db import models
from .employee import Employee
from .membership import Membership

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    membership_id = models.ForeignKey(Membership, on_delete=models.CASCADE)
    points_earned = models.IntegerField()
    transaction_date = models.DateField()

    def __str__(self):
        return self.transaction_id
