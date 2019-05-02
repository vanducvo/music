from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#User Entity
class User(AbstractUser):
    GENDER_TYPES = (('m','male'), ('f','female'), ('o','other'))
    gender = models.CharField(max_length = 6, choices = GENDER_TYPES, default ='other')

#Song Entity
class Song(models.Model):
    title = models.CharField(max_length = 200)
    image = models.ImageField(upload_to = 'image')
    audio = models.FileField(upload_to='audio')
    lyric = models.CharField(max_length = 1000)
    producer =  models.ForeignKey(User, on_delete = models.DO_NOTHING)

#Artist Entity
class Artist(models.Model):
    GENDER_TYPES = (('m','male'), ('f','female'), ('o','other'))
    name = models.CharField(max_length = 100)
    gender = models.CharField(max_length = 6, choices = GENDER_TYPES, default ='other')

#Block list Entity
class Blocklist(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)

#RoomListen
class RoomListen(models.Model):
    name = models.CharField(max_length = 100)
    topic = models.CharField(max_length = 50)
    password = models.CharField(max_length=256)

#Playist Entity
class Playist(models.Model):
    name = models.CharField(max_length = 100)
    room = models.ForeignKey(RoomListen, on_delete = models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)

#Messenge Entity
class Messenge(models.Model):
    user = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    room = models.ForeignKey(RoomListen, on_delete = models.DO_NOTHING)
    content = models.CharField(max_length=1000)

#Song In Playist Relation
class SongInPlayist(models.Model):
    playist = models.ForeignKey(Playist, on_delete = models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete = models.DO_NOTHING)

#Artist Sing Song Relation
class ArtistSingSong(models.Model):
    artist = models.ForeignKey(Artist, on_delete = models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete = models.DO_NOTHING)

#Block list Song Relation
class BlocklistSong(models.Model):
    blocklist = models.ForeignKey(Blocklist, on_delete = models.DO_NOTHING)
    song = models.ForeignKey(Song, on_delete = models.DO_NOTHING)

#Procedure Artist Relation
class ArtistOfProcedure(models.Model):
    artist = models.ForeignKey(Artist, on_delete = models.DO_NOTHING)
    procedure = models.ForeignKey(User, on_delete = models.DO_NOTHING)