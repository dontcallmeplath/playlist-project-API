from django.db import models

class PlaylistEpisode(models.Model):
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE, related_name='playlist_episode')
    playlist = models.ForeignKey("Playlist", on_delete=models.CASCADE, related_name='playlist')