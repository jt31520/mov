from django.db import models

# Create your models here.

class video_detail(models.Model):
    name = models.CharField(max_length=255)
    nameMd5 = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    updateTo = models.CharField(max_length=255)
    score = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    star = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    issueTime = models.CharField(max_length=255)
    filmLength = models.CharField(max_length=255)
    updateTime = models.CharField(max_length=255)
    details = models.TextField(default="")
    totalPlay = models.CharField(max_length=255)
    todayPlay = models.CharField(max_length=255)
    totalScore = models.CharField(max_length=255)
    scoreTime = models.CharField(max_length=255)
    source = models.CharField(max_length=255)

class video_episode(models.Model):
    name = models.CharField(max_length=255)
    nameMd5 = models.CharField(max_length=255)
    episode = models.CharField(max_length=255)
    episodeUrl = models.CharField(max_length=255)
    episodeMd5 = models.CharField(max_length=255)


