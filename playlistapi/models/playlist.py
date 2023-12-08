from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=155)
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE, related_name='episode')
    creator = models.ForeignKey("Creator", on_delete=models.CASCADE, related_name='playlist_creator')