from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
  email = models.EmailField(unique=True)
  REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']