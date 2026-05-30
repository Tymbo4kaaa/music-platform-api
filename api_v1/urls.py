from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, ArtistViewSet, AlbumViewSet, TrackViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'artists', ArtistViewSet, basename='artist')
router.register(r'albums', AlbumViewSet, basename='album')
router.register(r'tracks', TrackViewSet, basename='track')
router.register(r'playlists', PlaylistViewSet, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
]