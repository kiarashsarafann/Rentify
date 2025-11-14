from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, blank=False, null=False)
    national_code = models.CharField(max_length=10, blank=False, null=False)