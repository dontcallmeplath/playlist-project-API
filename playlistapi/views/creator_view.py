from rest_framework.viewsets import ViewSet
from rest_framework import serializers
from playlistapi.models import Creator

class CreatorView(ViewSet):
    pass

class CreatorSerializer(serializers.ModelSerializer):
    """Playlist Creator view"""
    class Meta:
        model = Creator
        fields = ('id', 'bio', 'profile_image_url', 'created_on', 'active', 'user_id')