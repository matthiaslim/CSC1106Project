from django.db import models

class Membership(models.Model):

    COUNTRY_CHOICES = [
        ('Singapore', 'Singapore'),
        ('Malaysia', 'Malaysia'),
        ('China', 'China')
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive')
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    ]

    member_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="Male")
    address = models.CharField(max_length=255)
    phone_number = models.IntegerField()
    email_address = models.EmailField(max_length=100)
    country = models.CharField(max_length=200, choices=COUNTRY_CHOICES, default="Singapore")
    membership_level = models.CharField(max_length=50)
    points = models.IntegerField()
    points_expiry_date = models.DateField()
    member_expiry_date = models.DateField()
    membership_status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="Active")  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"