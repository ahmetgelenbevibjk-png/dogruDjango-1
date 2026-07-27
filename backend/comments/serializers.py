from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Comment

User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class CommentSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)


    username = serializers.ReadOnlyField(source='user.username')
    user_name = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'username', 'user_name', 'content', 'created_at']
        read_only_fields = ['user']