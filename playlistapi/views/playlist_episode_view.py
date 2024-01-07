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
        fields = ['id', 'playlist',]


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
        """Handle POST operations

        Returns
            Response -- JSON serialized playlist instance
        """
        episode = request.data.get("episode_id")
        playlist = request.data.get("playlist_id")

        playlist_episode = PlaylistEpisode.objects.create(
            episode_id=episode,
            playlist_id=playlist,
        )

        try:
            serializer = PlaylistEpisodeSerializer(
                playlist_episode, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item on playlist episode

        Returns:
            Response -- empty response body
        """
        creator = self.request.query_params.get('creator_id', None)

        try:
            playlist_episode = PlaylistEpisode.objects.get(pk=pk)

            if pk:
                playlist_episode.delete()
                return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You do not have admin rights or invalid parameters"}, status=status.HTTP_403_FORBIDDEN)

        except PlaylistEpisode.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
