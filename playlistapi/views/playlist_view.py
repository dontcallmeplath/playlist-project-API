# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from .creator_view import CreatorSerializer
from .episode_view import EpisodeListSerializer
from playlistapi.models import Creator, Playlist, Episode
from django.contrib.auth.models import User


class PlaylistSerializer(ModelSerializer):
    # creator_id = CreatorSerializer(many=False).fields['id']
    # episode = EpisodeSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = '__all__'


class PlaylistView(ViewSet):
    def list(self, request):
        # get query parameters from request for specific user
        creator = self.request.query_params.get('creator_id', None)

        # filter to allow for all and specific user's playlists
        # if checks for specific user
        if creator is not None and creator == "current":
            playlists = Playlist.objects.filter(
                creator__user=request.auth.user_id)
        else:
            # otherwise get all playlists & filter by approved and dates in the past
            playlists = Playlist.objects.all().order_by("-id")

        serializer = PlaylistSerializer(
            playlists, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for a single playlist

        Returns:
            Response -- JSON serialized object
        """
        try:
            playlist = Playlist.objects.get(pk=pk)
            # Get associated tags for playlist

            playlist_serializer = PlaylistSerializer(
                playlist, context={"request": request})
            playlist_data = playlist_serializer.data

            return Response(playlist_data, status=status.HTTP_200_OK)
        except Playlist.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single playlist

        Returns:
            Response -- empty response body
        """
        try:
            playlist = Playlist.objects.get(pk=pk)
            if playlist.creator.user_id == request.user.id or request.user.is_staff:
                playlist.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            return Response({"message": "You are not the creator of this playlist."}, status=status.HTTP_403_FORBIDDEN)
        except Playlist.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk=None):
        """Handle PUT requests for a single playlist

        Returns:
            Response -- JSON serialized object
        """
        try:
            playlist = Playlist.objects.get(pk=pk)

            # Check if the user is the creator of the playlist
            if playlist.creator.user_id != request.user.id:
                return Response({"message": "You are not the creator of this playlist."}, status=status.HTTP_403_FORBIDDEN)

            serializer = PlaylistSerializer(
                playlist, data=request.data, partial=True)

            if serializer.is_valid():
                # Update only the provided fields
                serializer.save()

                # Re-serialize the playlist to include related data
                updated_playlist = Playlist.objects.get(pk=pk)
                serialized_playlist = PlaylistSerializer(
                    updated_playlist, context={"request": request})

                return Response(serialized_playlist.data, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Playlist.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized playlist instance
        """

        creator = Creator.objects.get(user=request.user.id)
        # episode_id = Episode.objects.get(pk=request.data['episode_id'])
        title = request.data.get("name")

        playlist = Playlist.objects.create(
            creator=creator,
            # episode = episode_id,
            name=title,
        )

        try:
            serializer = PlaylistSerializer(
                playlist, context={"request": request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(ex, status=status.HTTP_400_BAD_REQUEST)
