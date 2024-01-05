from django.db import models
# from django.contrib.auth.models import User

class Episode(models.Model):
    series_name = models.CharField(max_length=155)
    episode_name = models.CharField(max_length=155)
    serial = models.CharField(max_length=10)
    # will use Textarea for the form field
    description = models.TextField()
    image = models.URLField(max_length=155)
    # TV-Y, TV-Y7, TV-G, TV-PG, TV-14, TV-MA
    rating = models.CharField(max_length=5)
    tag = models.ManyToManyField("Tag", through='EpisodeTag')
    playlist = models.ManyToManyField("Playlist", through='PlaylistEpisode')
