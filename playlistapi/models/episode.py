from django.db import models
# from django.contrib.auth.models import User

class Episode(models.Model):
    series_name = models.CharField(max_length=155)
    episode_name = models.CharField(max_length=155)
    serial = models.SlugField(default="", null=False)
    # will use Textarea for the form field
    description = models.TextField()
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=155)
    # TV-Y, TV-Y7, TV-Y7 FV, TV-G, TV-PG, TV-14, TV-MA
    rating = models.CharField(max_length=4)