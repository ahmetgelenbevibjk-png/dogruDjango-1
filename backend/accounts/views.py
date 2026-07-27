from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
)




class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return CustomUserSerializer

    def get_object(self):
        pk_or_username = self.kwargs.get('pk') or self.kwargs.get('username')

        if pk_or_username:
            if str(pk_or_username).isdigit():
                obj = get_object_or_404(CustomUser, pk=pk_or_username)
            else:
                obj = get_object_or_404(CustomUser, username=pk_or_username)

            self.check_object_permissions(self.request, obj)
            return obj

        return super().get_object()


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]




