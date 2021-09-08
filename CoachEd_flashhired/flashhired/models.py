from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class User(AbstractUser):
    phone_number = PhoneNumberField()
    is_admin=models.BooleanField(default=False)
    is_candidate=models.BooleanField(default=False)
    is_recruiter=models.BooleanField(default=False)
