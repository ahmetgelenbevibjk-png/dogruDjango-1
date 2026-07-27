from rest_framework import serializers
from .models import Album, AlbumImage

class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ['id', 'image', 'created_at']

class AlbumSerializer(serializers.ModelSerializer):
    images = AlbumImageSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'title', 'description', 'created_at', 'images']