from django.contrib.auth import get_user_model
from rest_framework import serializers
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
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'user',
            'username',
            'user_name',
            'content',
            'parent',
            'created_at',
            'replies'
        ]
        read_only_fields = ['user']

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []