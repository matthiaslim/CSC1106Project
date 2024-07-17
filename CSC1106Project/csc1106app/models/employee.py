from django.db import models
from .user import User
from .department import Department

class Employee(models.Model):
    HOURLY_RATES = {
        'Chairman': 100,
        'Manager': 70,
        'Employee': 50,
        'HR': 30,
    }

    employee_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    job_title = models.CharField(max_length=50)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    hire_date = models.DateField()
    contract_expiry_date = models.DateField(null=True, blank=True)
    employee_role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='employee_images/', null=True, blank=True)
    onboarded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def hourly_rate(self):
        return self.HOURLY_RATES.get(self.job_title, 0)

    def calculate_hours_worked(self, start_date, end_date):
        from .attendance import Attendance
        attendance_records = Attendance.objects.filter(
            employee=self,
            time_in__gte=start_date,
            time_out__lte=end_date
        )
        total_hours = sum(
            (record.time_out - record.time_in).total_seconds() / 3600
            for record in attendance_records if record.time_out
        )
        return total_hours
