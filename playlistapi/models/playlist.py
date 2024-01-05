from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=155)
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name='playlist_creator')