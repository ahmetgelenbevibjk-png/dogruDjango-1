import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


class BaseModel(models.Model):

    id=(models.UUIDField
        (
        primary_key=True , default=uuid.uuid4,editable=False, unique=True
        ))

    is_active=models.BooleanField(default=True)

    created_user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
    )
    updated_user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
    )
    deleted_user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_deleted',
    )

    created_at=models.DateTimeField(default=timezone.now, editable=False)
    updated_at=models.DateTimeField(auto_now=True)
    deleted_at=models.DateTimeField(null=True,blank=True)

    class Meta:
        abstract= True


def soft_delete(self,user=None):
            """Kaydı veritabanından silmek yerine pasif hale getirir"""
            self.is_active=False
            self.deleted_at=timezone.now()
            if user and user.is_authenticated:
                self.deleted_user=user
            self.save()