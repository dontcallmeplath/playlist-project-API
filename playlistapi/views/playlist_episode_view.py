from rest_framework.serializers import ModelSerializer
# from .episode_view import EpisodeSerializer
# from .playlist_view import PlaylistSerializer
# from .creator_view import CreatorSerializer
from playlistapi.models import PlaylistEpisode, Episode, Playlist
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'rating', 'image', 'series_name', 'episode_name',
                  'description',]


class PlaylistSerializer(ModelSerializer):
    episode = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'creator', 'name', 'episode',]


class PlaylistEpisodeSerializer(ModelSerializer):

    # episode = EpisodeSerializer(many=True, read_only=True)
    playlist = PlaylistSerializer(many=False)

    class Meta:
        model = PlaylistEpisode
        fields = ['playlist',]


class PlaylistEpisodeView(ViewSet):
    """Playlist Episodes view"""

    def list(self, request):
        """Handle GET requests for all playlist episodes

        Returns:
            Response -- JSON serialized array
        """
        creator = self.request.query_params.get('creator_id', None)
        playlist_query = self.request.query_params.get('playlist_id', None)

        if creator is not None and creator == "current":
            creator_playlists = PlaylistEpisode.objects.all().filter(
                playlist__creator_id=request.auth.user_id)
            if playlist_query is not None:
                playlist_episodes = creator_playlists.all().filter(
                    playlist__id=playlist_query)
            else:
                playlist_episodes = creator_playlists

        else:
            return Response({"message": "This creator hasn't added playlists yet."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PlaylistEpisodeSerializer(playlist_episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = PlaylistEpisodeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
