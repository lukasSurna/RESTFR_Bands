from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Band(models.Model):
    name = models.CharField(_("name"), max_length=200)
    description = models.TextField(_("description"), max_length=3000, default='')

    def __str__(self):
        return f"{self.name}"


class Album(models.Model):
    name = models.CharField(_("name"), max_length=100)
    band = models.ForeignKey(
        Band, 
        on_delete=models.CASCADE, 
        related_name='albums',
    )

    def __str__(self):
        return f"{self.name}"


class Song(models.Model):
    name = models.CharField(_("name"), max_length=100)
    duration = models.IntegerField()
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        related_name='songs',
    )

    def __str__(self):
        return f"{self.name} - {self.duration}"


class AlbumReview(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    album = models.ForeignKey(
        Album, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    content = models.TextField(max_length=2000)


    def __str__(self):
        return f'{self.album.name} Review'


class AlbumReviewComment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    album_review = models.ForeignKey(
        AlbumReview, 
        on_delete=models.CASCADE, 
        related_name='comments',
    )
    content = models.TextField(max_length=1000)

    def __str__(self):
        return f"Comment by {self.user} on {self.album_review}"


class AlbumReviewLike(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
    )
    album_review = models.ForeignKey(
        AlbumReview, 
        on_delete=models.CASCADE, 
        related_name='likes',
    )
    
    def __str__(self):
        return f'{self.user} likes {self.album_review}'