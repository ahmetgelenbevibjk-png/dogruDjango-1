from rest_framework import serializers
from .models import Album, AlbumImage

class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlbumImage
        fields = ['id', 'album', 'image', 'created_at'] # <-- 'album' alanını buraya ekledik

class AlbumSerializer(serializers.ModelSerializer):
    images = AlbumImageSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Album
        fields = ['id', 'user', 'username', 'title', 'description', 'created_at', 'images']
        read_only_fields = ['user']