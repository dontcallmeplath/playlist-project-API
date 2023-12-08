from django.db import models

class EpisodeTag(models.Model):
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE, related_name='tag')
    episode = models.ForeignKey("Episode", on_delete=models.CASCADE, related_name='episode_tag')