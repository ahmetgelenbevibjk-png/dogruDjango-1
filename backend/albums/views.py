from core.views import BaseModelViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Album, AlbumImage
from .serializers import AlbumSerializer, AlbumImageSerializer

class AlbumViewSet(BaseModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]
    queryset = Album.objects.all() # <-- Bu satırı ekledik

    def get_queryset(self):
        queryset = Album.objects.all().order_by('-created_at')
        user_id = self.request.query_params.get('user')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AlbumImageViewSet(BaseModelViewSet):
    serializer_class = AlbumImageSerializer
    permission_classes = [IsAuthenticated]
    queryset = AlbumImage.objects.all() # <-- Bu satırı ekledik

    def get_queryset(self):
        return AlbumImage.objects.all().order_by('-created_at')