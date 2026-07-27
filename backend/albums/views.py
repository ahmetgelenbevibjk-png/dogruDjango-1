from rest_framework import viewsets
from .models import Album ,AlbumImage
from .serializers import AlbumSerializer,AlbumImageSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('-created_at')
    serializer_class = AlbumSerializer

class AlbumImageViewSet(viewsets.ModelViewSet):
    queryset = AlbumImage.objects.all().order_by('-created_at')
    serializer_class = AlbumImageSerializer