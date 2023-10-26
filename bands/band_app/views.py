from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, mixins, status, response
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models
from . import serializers

User = get_user_model()

class UserCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]
    
    def delete(self, *args, **kwargs):
        user = User.objects.filter(pk=self.request.user.pk)
        if user.exists():
            user.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('User does not exist')


class BandList(generics.ListCreateAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BandDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Band.objects.all()
    serializer_class = serializers.BandSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        name = models.Band.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if name.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only delete your added Bands'))

    def put(self, request, *args, **kwargs):
        name = models.Band.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if name.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_('You can only delete your added Bands'))

class AlbumList(generics.ListCreateAPIView):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer

class AlbumDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer

class SongList(generics.ListCreateAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer

class AlbumReviewList(generics.ListCreateAPIView):
    queryset = models.AlbumReview.objects.all()
    serializer_class = serializers.AlbumReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

class AlbumReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AlbumReview.objects.all()
    serializer_class = serializers.AlbumReviewSerializer

    def delete(self, request, *args, **kwargs):
        review = models.AlbumReview.objects.filter(
            pk=kwargs['pk'], 
            user=self.request.user,
        )
        if review.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can delete only yours review!"))


    def put(self, request, *args, **kwargs):
        review = models.AlbumReview.objects.filter(
            pk=kwargs['pk'],
            user=self.request.user,
        )
        if review.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You can edit only yours review"))


class AlbumReviewCommentList(generics.ListCreateAPIView):
    queryset = models.AlbumReviewComment.objects.all()
    serializer_class = serializers.AlbumReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        review = models.AlbumReview.objects.get(pk=self.kwargs['pk'])
        return models.AlbumReviewComment.objects.filter(album_review=review)

    def perform_create(self, serializer):
        review = models.AlbumReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, album_review=review)


class AlbumReviewCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.AlbumReviewComment.objects.all()
    serializer_class = serializers.AlbumReviewCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        comment = models.AlbumReviewComment.objects.filter(
            pk=kwargs['pk'], 
            user=self.request.user,
        )
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError("You're trying to delete someone else's comment!")

    def put(self, request, *args, **kwargs):
        comment = models.AlbumReviewComment.objects.filter(
            pk=kwargs['pk'], 
            user=self.request.user,
        )
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError("You're trying to edit someone else's comment!")

class AlbumReviewLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.AlbumReviewLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        review = models.AlbumReview.objects.get(pk=self.kwargs['pk'])
        return models.AlbumReviewLike.objects.filter(user=user, album_review=review)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already liked this review!')
        user = self.request.user
        review = models.AlbumReview.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=user, album_review=review)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You haven\'t liked this review before!')


