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
        episode_tags = EpisodeTag.objects.all()
        serializer = EpisodeTagSerializer(episode_tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = EpisodeTagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item on playlist episode

        Returns:
            Response -- "Delete successful"
        """
        creator = self.request.query_params.get('creator_id', None)

        try:
            episode_tag = EpisodeTag.objects.get(pk=pk)

            if pk:
                episode_tag.delete()
                return Response({"message": "Delete successful"}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You do not have admin rights or invalid parameters"}, status=status.HTTP_403_FORBIDDEN)

        except EpisodeTag.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
