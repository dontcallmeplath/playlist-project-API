# from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from playlistapi.models import EpisodeTag

class EpisodeTagSerializer(ModelSerializer):

    class Meta:
        model = EpisodeTag
        fields = ["id", "episode", "tag"]

class EpisodeTagView(ViewSet):
    """Playlist Episode Tags view"""
    def list(self, request):
        """Handle GET requests for all episode tags
        
        Returns:
            Response -- JSON serialized array
        """
        episode_tags= EpisodeTag.objects.all()
        serializer = EpisodeTagSerializer(episode_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = EpisodeTagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)