from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer 
from rest_framework import status
from playlistapi.models import Tag

class TagView(ViewSet):
    """Playlist tags view"""

    def list(self, request):
        """Handle GET requests for all tags

        Returns:
            Response -- JSON serialized array
        """
        tags = Tag.objects.all().order_by('label')
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single tag

        Returns:
            Response -- JSON serialized object
        """
        try:
            tag = Tag.objects.get(pk=pk)
            serializer = TagSerializer(tag, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Tag.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single tag

        Returns:
            Response -- empty response body
        """
        try:
            tag = Tag.objects.get(pk=pk)
            if request.user.is_staff:
                tag.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You do not have admin rights"}, status=status.HTTP_403_FORBIDDEN)
        except Tag.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def update(self, request, pk):
        """Handle PUT requests for a single tag

        Returns:
            Response -- JSON serialized object
        """
        try:
            tag = Tag.objects.get(pk=pk)
            if request.user.is_staff:
                serializer = TagSerializer(data=request.data)
                if serializer.is_valid():
                    tag.label = serializer.validated_data["label"]
                    tag.save()

                    serializer = TagSerializer(tag, context={"request": request})
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You do not have admin rights"}, status=status.HTTP_403_FORBIDDEN)
        except Tag.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
            
    
    def create(self, request):
        label = request.data.get('label')

        tag = Tag.objects.create(
            label=label
        )
        serializer = TagSerializer(tag, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
