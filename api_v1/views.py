from django.utils.decorators import method_decorator
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_extensions.cache.decorators import cache_response

from .models import Genre, Artist, Album, Track, Playlist, PlaylistTrack, Like
from .serializers import (
    GenreSerializer, ArtistSerializer, AlbumSerializer, 
    TrackSerializer, PlaylistSerializer, LikeSerializer
)


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с жанрами музыки"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs
    
    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, 
                       status=status.HTTP_201_CREATED,
                       headers=self.get_success_headers(serializer.data))
    
    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Genre.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Genre.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, 
                                           partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='batch')
    def batch_delete(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({'error': 'Parameter "ids" is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        ids_list = [int(pk) for pk in ids.split(',')]
        self.queryset.filter(pk__in=ids_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArtistViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с исполнителями"""
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        country = self.request.query_params.get('country')
        if name:
            qs = qs.filter(name__icontains=name)
        if country:
            qs = qs.filter(country__iexact=country)
        return qs
    
    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                       status=status.HTTP_201_CREATED,
                       headers=self.get_success_headers(serializer.data))
    
    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Artist.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Artist.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data,
                                           partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='batch')
    def batch_delete(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({'error': 'Parameter "ids" is required'},
                          status=status.HTTP_400_BAD_REQUEST)
        ids_list = [int(pk) for pk in ids.split(',')]
        self.queryset.filter(pk__in=ids_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='albums')
    def get_albums(self, request, pk=None):
        """Получить все альбомы исполнителя"""
        artist = self.get_object()
        albums = Album.objects.filter(artist=artist)
        serializer = AlbumSerializer(albums, many=True, context={'request': request})
        return Response(serializer.data)


class AlbumViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с альбомами"""
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        artist_id = self.request.query_params.get('artist_id')
        genre_id = self.request.query_params.get('genre_id')
        year = self.request.query_params.get('year')
        title = self.request.query_params.get('title')
        
        if artist_id:
            qs = qs.filter(artist_id=artist_id)
        if genre_id:
            qs = qs.filter(genre_id=genre_id)
        if year:
            qs = qs.filter(release_date__year=year)
        if title:
            qs = qs.filter(title__icontains=title)
        return qs
    
    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                       status=status.HTTP_201_CREATED,
                       headers=self.get_success_headers(serializer.data))
    
    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Album.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Album.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data,
                                           partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='batch')
    def batch_delete(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({'error': 'Parameter "ids" is required'},
                          status=status.HTTP_400_BAD_REQUEST)
        ids_list = [int(pk) for pk in ids.split(',')]
        self.queryset.filter(pk__in=ids_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['get'], url_path='tracks')
    def get_tracks(self, request, pk=None):
        """Получить все треки альбома"""
        album = self.get_object()
        tracks = Track.objects.filter(album=album).order_by('track_number')
        serializer = TrackSerializer(tracks, many=True, context={'request': request})
        return Response(serializer.data)


class TrackViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с треками"""
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        qs = super().get_queryset()
        artist_id = self.request.query_params.get('artist_id')
        album_id = self.request.query_params.get('album_id')
        genre_id = self.request.query_params.get('genre_id')
        title = self.request.query_params.get('title')
        min_duration = self.request.query_params.get('min_duration')
        max_duration = self.request.query_params.get('max_duration')
        
        if artist_id:
            qs = qs.filter(artist_id=artist_id)
        if album_id:
            qs = qs.filter(album_id=album_id)
        if genre_id:
            qs = qs.filter(genre_id=genre_id)
        if title:
            qs = qs.filter(title__icontains=title)
        if min_duration:
            qs = qs.filter(duration__gte=int(min_duration))
        if max_duration:
            qs = qs.filter(duration__lte=int(max_duration))
        return qs
    
    @cache_response(60 * 15)
    def retrieve(self, request, *args, **kwargs):
        track = self.get_object()
        track.play_count += 1
        track.save(update_fields=['play_count'])
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                       status=status.HTTP_201_CREATED,
                       headers=self.get_success_headers(serializer.data))
    
    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Track.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Track.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data,
                                           partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='batch')
    def batch_delete(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({'error': 'Parameter "ids" is required'},
                          status=status.HTTP_400_BAD_REQUEST)
        ids_list = [int(pk) for pk in ids.split(',')]
        self.queryset.filter(pk__in=ids_list).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post', 'delete'], url_path='like')
    def toggle_like(self, request, pk=None):
        """Добавить или удалить лайк у трека"""
        track = self.get_object()
        user = request.user
        
        if request.method == 'POST':
            like, created = Like.objects.get_or_create(user=user, track=track)
            serializer = LikeSerializer(like)
            status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
            return Response(serializer.data, status=status_code)
        else:
            Like.objects.filter(user=user, track=track).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с плейлистами"""
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        from django.db.models import Q
        qs = Playlist.objects.all()
        if not self.request.user.is_superuser:
            qs = qs.filter(Q(user=self.request.user) | Q(is_public=True))
        return qs
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @cache_response(60 * 10)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data,
                       status=status.HTTP_201_CREATED,
                       headers=self.get_success_headers(serializer.data))
    
    def update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Playlist.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def partial_update(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        if many:
            instances = [Playlist.objects.get(pk=item['id']) for item in request.data]
            serializer = self.get_serializer(instances, data=request.data,
                                           partial=True, many=True)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    @action(detail=False, methods=['delete'], url_path='batch')
    def batch_delete(self, request):
        ids = request.query_params.get('ids')
        if not ids:
            return Response({'error': 'Parameter "ids" is required'},
                          status=status.HTTP_400_BAD_REQUEST)
        ids_list = [int(pk) for pk in ids.split(',')]
        self.queryset.filter(pk__in=ids_list, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['post'], url_path='add-track')
    def add_track(self, request, pk=None):
        """Добавить трек в плейлист"""
        playlist = self.get_object()
        track_id = request.data.get('track_id')
        position = request.data.get('position', playlist.playlist_tracks.count())
        
        if not track_id:
            return Response({'error': 'track_id is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        track = Track.objects.get(pk=track_id)
        playlist_track, created = PlaylistTrack.objects.get_or_create(
            playlist=playlist,
            track=track,
            defaults={'position': position}
        )
        serializer = PlaylistTrackSerializer(playlist_track)
        return Response(serializer.data, 
                       status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
    
    @action(detail=True, methods=['delete'], url_path='remove-track')
    def remove_track(self, request, pk=None):
        """Удалить трек из плейлиста"""
        playlist = self.get_object()
        track_id = request.query_params.get('track_id')
        
        if not track_id:
            return Response({'error': 'track_id query parameter is required'},
                          status=status.HTTP_400_BAD_REQUEST)
        
        PlaylistTrack.objects.filter(playlist=playlist, track_id=track_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
