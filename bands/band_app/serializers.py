from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Band
        fields = ['id', 'name']


class AlbumSerializer(serializers.ModelSerializer):
    band = serializers.CharField(read_only=True, source='band.name')

    class Meta:
        model = models.Album
        fields = ['id', 'band', 'name']


class SongSerializer(serializers.ModelSerializer):
    album_name = serializers.CharField(read_only=True, source='album.name')
    band_name = serializers.CharField(
        read_only=True, source='album.band.name')

    class Meta:
        model = models.Song
        fields = ['name', 'duration', 'album', 'album_name', 'band_name']


class AlbumReviewCommentSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    user_id = serializers.ReadOnlyField(source='user.id')
    album_review_id = serializers.ReadOnlyField(source='album_review.id')

    class Meta:
        model = models.AlbumReviewComment
        fields = ['id', 'user_id', 'username', 'album_review_id', 'content']


class AlbumReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True, source='user.username')
    album_name = serializers.CharField(read_only=True, source='album.name')
    band_name = serializers.CharField(read_only=True, source='album.band.name')
    user_id = serializers.CharField(read_only=True, source='user.id')
    comments = AlbumReviewCommentSerializer(read_only=True, many=True)
    comment_count = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    
    class Meta:
        model = models.AlbumReview
        fields = [
        'id', 'user_id', 'user_name', 'album_id',
        'album_name', 'band_name', 'content', 'score', 'comments', 'comment_count', 'likes'
        ]

    def get_comment_count(self, obj):
        return models.AlbumReviewComment.objects.filter(album_review=obj).count()

    def get_likes(self, obj):
        return models.AlbumReviewLike.objects.filter(album_review=obj).count()

class AlbumReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumReviewLike
        fields = ['id']