from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from core.models import BaseModel


class Company(BaseModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)

    ROLE_CHOICES =(
        ('admin','Admin'),
        ('moderator','Moderatör'),
        ('user','kullanıcı'),
                   )

    role=models.CharField(max_length=20, choices=ROLE_CHOICES,default='user')


    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name="Çalıştığı Şirket"
    )

    def __str__(self):
        return self.username


class Address(BaseModel):
    # null=True eklendi ki serializer'da hata almadan oluşturulabilsin
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='address'
    )
    street = models.CharField(max_length=255, blank=True, null=True)
    suite = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    lat = models.CharField(max_length=50, blank=True, null=True)
    lng = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f'{self.user.username if self.user else "No User"} - Address'


class UserProfile(BaseModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - Profile'