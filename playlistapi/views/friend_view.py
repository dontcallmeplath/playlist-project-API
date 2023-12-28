from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import status
from django.contrib.auth.models import User
from playlistapi.models import Friend, Creator

class FriendView(ViewSet):
    def list(self, request):
        # get query parameters from request for specific user
        creator = self.request.query_params.get('creator', None)

        # filter to allow for all and specific user's friends
        # if checks for specific user
        if creator is not None and creator == "current":
            friends = Friend.objects.filter(creator__user=request.auth.user)
        else:
            return Response({"message": "This creator hasn't added friends yet."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FriendSerializer(friends, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single Friend

        Returns:
            Response -- JSON serialized object
        """
        try:
            friend = Friend.objects.get(pk=pk)
            serializer = FriendSerializer(friend, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Friend.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        email = request.data.get('email')
        creator_id = Creator.objects.get(user=request.user.id)

        friend = Friend.objects.create(
            email=email,
            creator=creator_id,
        )

        serializer = FriendSerializer(friend, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        try:
            friend = Friend.objects.get(pk=pk)
            if request.user.is_staff:
                serializer = FriendSerializer(data=request.data)
                if serializer.is_valid():
                    friend.email = serializer.validated_data["email"]
                    friend.save()

                    serializer = FriendSerializer(friend, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You don't have admin privileges"}, status=status.HTTP_403_FORBIDDEN)
        except Friend.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a singular Friend

        Returns:
            Response -- 204, 403, 404, or 500 status
        """
        try:
            friend = Friend.objects.get(pk=pk)
            if request.user.is_staff:
                friend.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "You don't have admin rights!"}, status=status.HTTP_403_FORBIDDEN)          
        except Friend.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# class UserSerializer(ModelSerializer):
#     """JSON serializer for user tied to creator"""

#     full_name = SerializerMethodField('get_full_name')

#     def get_full_name(self, obj):
#         return f'{obj.first_name} {obj.last_name}'

#     class Meta:
#         model = User
#         fields = ("full_name",)

# class CreatorSerializer(ModelSerializer):
#     """JSON serializer for creator of friend"""

#     user = UserSerializer(many=False)

#     class Meta:
#         model = Creator
#         fields = ("id", "user",)

class FriendSerializer(ModelSerializer):
    """JSON serializer for friends"""

    # creator = CreatorSerializer(many=False)

    # def get_is_creator(self, obj):
    #     user = None
    #     request = self.context.get("request")
    #     if request and hasattr(request, "user"):
    #         user = request.user
    #     return user == obj.creator.user

    class Meta:
        model = Friend
        fields = ("creator_id", "email", "name", "id")        
