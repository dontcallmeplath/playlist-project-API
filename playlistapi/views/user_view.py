from rest_framework import status, permissions
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from playlistapi.models import Creator
from .creator_view import CreatorSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name', 'last_name')  # add other fields as needed
        extra_kwargs = {'password': {'write_only': True}}



class UserView(ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['email'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name']
            )
            
            token = Token.objects.create(user=user)

            data = {
                'valid': True,
                'token': token.key,
                'staff': user.is_staff,
                'id': user.id,
                'name': user.first_name
            }

            creator = Creator.objects.create(
                bio = request.data.get("bio"),
                user = User.objects.get(username=request.data['username'])
            )

            try: 
                creator_serializer = CreatorSerializer(creator, context={"request": request})
            except:
                return Response(creator_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        '''Handles the authentication of a user

        Method arguments:
        request -- The full HTTP request object
        '''
        username = request.data['username']
        password = request.data['password']

        # Use the built-in authenticate method to verify
        # authenticate returns the user object or None if no user is found
        authenticated_user = authenticate(username=username, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = {
                'valid': True,
                'token': token.key,
                'staff': token.user.is_staff,
                'id': token.user.id,
                'name': token.user.first_name
            }
            return Response(data)
        else:
            # Bad login details were provided. So we can't log the user in.
            data = { 'valid': False }
            return Response(data)

    def list(self, request):
        """Handle GET requests for all users
        
        Returns:
            Response -- JSON serialized array
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for a single User

        Returns:
            Response -- JSON serialized object
        """
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user, context={"request": request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist as ex:
            return Response({"message": ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
