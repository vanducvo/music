from django.db import models

#Artist DB
class Artist(models.Model):
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    introduc = models.TextField()

#Song DB
class Song(models.Model):
    name = models.CharField(max_length=50)
    #duration = models.DurationField(max_length=50)
    genre = models.CharField(max_length=50)
    lyrics = models.TextField()
    artist = models.CharField(max_length = 50)
    #artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    audio = models.FileField(upload_to='songs/')
