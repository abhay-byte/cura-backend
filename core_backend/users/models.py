# users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # You can add profile fields here later, e.g.:
    # date_of_birth = models.DateField(null=True, blank=True)
    # health_goals = models.TextField(blank=True)
    email = models.EmailField(unique=True) # Make email the unique identifier

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email