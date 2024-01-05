from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from playlistapi.models import Creator

class CreatorSerializer(serializers.ModelSerializer):
    """Playlist Creator view"""
    class Meta:
        model = Creator
        fields = ('id', 'bio', 'profile_image', 'created_on', 'user_id')

class CreatorView(ViewSet):
    pass        