from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from playlistapi.models import Episode

class EpisodeSerializer(ModelSerializer):
    class Meta:
        model = Episode
        fields = ['id', 'series_name', 'episode_name', 'serial', 'description', 'image', 'rating']

class EpisodeView(ViewSet):
    """Playlist Episode view"""
    def list(self, request):
        """Handle GET requests for all episodes
        
        Returns:
            Response -- JSON serialized array
        """
        episodes= Episode.objects.all()
        serializer = EpisodeSerializer(episodes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EpisodeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)