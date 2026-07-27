from django.db import models
from core.models import BaseModel
class Album(BaseModel):
    title = models.CharField(max_length=200, verbose_name="Albüm Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    def __str__(self):
        return self.title

class AlbumImage(BaseModel):
    album = models.ForeignKey(Album, related_name='images', on_delete=models.CASCADE, verbose_name="Albüm")
    image = models.ImageField(upload_to='albums/', verbose_name="Fotoğraf")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.album.title} - Fotoğraf"