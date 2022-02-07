from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Profile, FollowRelation


class FollowRelationSerializer(serializers.ModelSerializer):
    followers_username = serializers.SerializerMethodField()
    following_username = serializers.SerializerMethodField()

    class Meta:
        model = FollowRelation
        fields = ['follower', 'following', 'followers_username', 'following_username']
        read_only_fields = ['follower']


    @staticmethod
    def get_followers_username(obj):
        return obj.user.username

    @staticmethod
    def get_following_username(obj):
        return obj.user.username


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ["follower"]
        read_only_fields = ["follower"]


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = ["following"]


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.SerializerMethodField()
    following = FollowingSerializer(many=True, read_only=True)
    followers = FollowersSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'name', 'following', 'followers', 'biography']

    @staticmethod
    def get_name(obj):
        return obj.user.get_full_name()

    @staticmethod
    def get_username(obj):
        return obj.user.username
