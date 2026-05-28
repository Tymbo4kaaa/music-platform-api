from django.db import models
from django.conf import settings

class Genre(models.Model):
    """Жанр музыки"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Artist(models.Model):
    """Исполнитель/Группа"""
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    formed_year = models.IntegerField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Album(models.Model):
    """Альбом исполнителя"""
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist, 
        on_delete=models.CASCADE, 
        related_name='albums'
    )
    release_date = models.DateField(null=True, blank=True)
    cover_url = models.URLField(blank=True)
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='albums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-release_date']
    
    def __str__(self):
        return f"{self.title} — {self.artist.name}"


class Track(models.Model):
    """Музыкальный трек"""
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name='tracks'
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tracks'
    )
    duration = models.PositiveIntegerField(help_text="Длительность в секундах")
    track_number = models.PositiveIntegerField(null=True, blank=True)
    audio_url = models.URLField(blank=True)
    play_count = models.PositiveIntegerField(default=0)
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tracks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['track_number', 'title']
    
    def __str__(self):
        return f"{self.title} — {self.artist.name}"


class Playlist(models.Model):
    """Плейлист пользователя"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='playlists'
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    cover_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"


class PlaylistTrack(models.Model):
    """Связь треков с плейлистом"""
    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='playlist_tracks'
    )
    track = models.ForeignKey(
        Track,
        on_delete=models.CASCADE,
        related_name='playlist_items'
    )
    added_at = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['position']
        unique_together = ['playlist', 'track']
    
    def __str__(self):
        return f"{self.playlist.title} → {self.track.title}"


class Like(models.Model):
    """Лайки пользователей к трекам"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'track']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} ❤️ {self.track.title}"