from rest_framework import serializers
from .models import Genre, Artist, Album, Track, Playlist, PlaylistTrack, Like


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']


class ArtistSerializer(serializers.ModelSerializer):
    albums_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Artist
        fields = ['id', 'name', 'bio', 'country', 'formed_year', 
                  'image_url', 'created_at', 'albums_count']
        read_only_fields = ['created_at']
    
    def get_albums_count(self, obj):
        return obj.albums.count()


class AlbumSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True
    )
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True, 
        required=False, allow_null=True
    )
    tracks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Album
        fields = ['id', 'title', 'artist', 'artist_id', 'release_date',
                  'cover_url', 'genre', 'genre_id', 'created_at', 'tracks_count']
        read_only_fields = ['created_at']
    
    def get_tracks_count(self, obj):
        return obj.tracks.count()


class TrackSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)
    artist_id = serializers.PrimaryKeyRelatedField(
        queryset=Artist.objects.all(), source='artist', write_only=True
    )
    album = AlbumSerializer(read_only=True)
    album_id = serializers.PrimaryKeyRelatedField(
        queryset=Album.objects.all(), source='album', write_only=True,
        required=False, allow_null=True
    )
    genre = GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True,
        required=False, allow_null=True
    )
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'artist_id', 'album', 'album_id',
                  'duration', 'track_number', 'audio_url', 'play_count',
                  'genre', 'genre_id', 'likes_count', 'created_at']
        read_only_fields = ['play_count', 'created_at']
    
    def get_likes_count(self, obj):
        return obj.likes.count()


class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    track_id = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(), source='track', write_only=True
    )
    
    class Meta:
        model = PlaylistTrack
        fields = ['id', 'track', 'track_id', 'added_at', 'position']


class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    tracks = PlaylistTrackSerializer(many=True, read_only=True, source='playlist_tracks')
    tracks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Playlist
        fields = ['id', 'user', 'title', 'description', 'is_public',
                  'cover_url', 'tracks', 'tracks_count', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_tracks_count(self, obj):
        return obj.playlist_tracks.count()


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    track = TrackSerializer(read_only=True)
    track_id = serializers.PrimaryKeyRelatedField(
        queryset=Track.objects.all(), source='track', write_only=True
    )
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'track', 'track_id', 'created_at']
        read_only_fields = ['user', 'created_at']