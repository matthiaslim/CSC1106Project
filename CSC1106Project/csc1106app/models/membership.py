from django.db import models

class Membership(models.Model):
    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=55)
    email_address = models.EmailField(max_length=100)
    country = models.CharField(max_length=200)
    membership_level = models.CharField(max_length=50)
    points = models.IntegerField()
    point_expiry_date = models.DateField()
    member_expiry_date = models.DateField()
    membership_status = models.CharField(max_length=100)