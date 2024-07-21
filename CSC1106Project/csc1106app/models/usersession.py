from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()  # This gets the user model defined in AUTH_USER_MODEL


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_id = models.CharField(max_length=40,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
