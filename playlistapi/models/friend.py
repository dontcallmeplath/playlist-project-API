from django.db import models
from django.contrib.auth.models import Creator

class Friend(models.Model):
    email = models.EmailField(max_length=155)
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE, related_name='creator')