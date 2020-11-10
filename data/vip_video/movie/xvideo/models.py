from django.db import models

# Create your models here.
class detail(models.Model):
    name = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    updateTime = models.CharField(max_length=255)
    episodeUrl = models.CharField(max_length=255)
    source = models.CharField(max_length=255)