from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    profile_image=models.ImageField(upload_to='Profile_img',blank=True)
    bio=models.TextField(blank=True)

    phone_regex = RegexValidator(
        regex=r'^\+?8801[3-9]\d{8}$',
        message="Phone number must be in Bangladeshi format: +8801XXXXXXXXX"
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=14,
        blank=True,
        null=True,
        unique=True
    )
    def __str__(self):
        return self.username