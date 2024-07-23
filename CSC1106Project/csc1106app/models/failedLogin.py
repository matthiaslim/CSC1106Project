from django.conf import settings
from django.db import models

class FailedLogin(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)