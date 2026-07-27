from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel


class CustomUser(AbstractUser):
    # JSONPlaceholder ana kullanıcı alanları
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Address(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='address'
    )
    street = models.CharField(max_length=255, blank=True, null=True)
    suite = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Address'


class Company(BaseModel):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name='company_detail'
    )
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Company'


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    # Profilde kalması mantıklı olan ekstra alanlar (Avatar vb.)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Profile'