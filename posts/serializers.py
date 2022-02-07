from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Post, Like


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.tracks = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user', 'post']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        exclude = ["timestamp"]

        validators = [
            UniqueTogetherValidator(
                queryset=Like.objects.all(),
                fields=['user', 'post'],
                message="liked before."
            )
        ]


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Post
        fields = ['username', 'content', 'name', 'likes', 'user', 'comments', 'is_liked', 'likes_count']

    @staticmethod
    def get_username(obj):
        return obj.user.username

    @staticmethod
    def get_likes_count(obj):
        return obj.likes.count()

    @staticmethod
    def get_name(obj):
        return obj.user.get_full_name()

    def get_is_liked(self, obj):
        user = self.context["request"].user
        if user and not user.is_anonymous:
            return bool(obj.likes.filter(user=user))
        return False

