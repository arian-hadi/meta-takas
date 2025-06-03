from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from datetime import timedelta
from .manager import UserManager

# Custom User Model
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']


    objects = UserManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# One-Time Password Model
class OneTimePassword(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(default=now)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def is_expired(self):
        return self.created_at < now() - timedelta(minutes=10)

    def __str__(self):
        return f"{self.user.username} passcode"


        