from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=11, unique=True)
    national_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
