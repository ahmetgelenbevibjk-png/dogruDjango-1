from django.contrib import admin
from .models import Album, AlbumImage

class AlbumImageInline(admin.TabularInline):
    model = AlbumImage
    extra = 4

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    inlines = [AlbumImageInline]
    list_display = ['title', 'created_at']

@admin.register(AlbumImage)
class AlbumImageAdmin(admin.ModelAdmin):
    list_display = ['album', 'created_at']
    