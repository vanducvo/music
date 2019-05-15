from django.shortcuts import render

from db import models
from django.utils.safestring import mark_safe
from django.db.models import Q
import json
import eyed3
import re
# Create your views here.
def index(request, song_id):
    partern = re.compile("^[0-9]+$")
    if not partern.match(song_id):
        return render(request, 'notify.html',{
            'infor': 'Không Có Bài Hát Này',
        })
    id =  int(song_id)
    mainsong = models.ArtistSingSong.objects.filter(song__pk__exact=id)
    if list(mainsong) == []:
        return render(request, 'notify.html',{
            'infor': 'Không Có Bài Hát Này',
        })

    maintitle = mainsong[0].song.title
    time = eyed3.load('/home/ducvovan/Source/main/music/music/' + mainsong[0].song.audio.url).info.time_secs
    duration = str(int(time/60)) + ":" + str(int(time)%60).zfill(2)

    for artist in mainsong:
        maintitle = maintitle + '-' + artist.artist.name
    
    mainsonginfo = [{
        'track': '',
        'name': maintitle,
        'duration': duration,
        'file': mainsong[0].song.audio.url
    }]

    likesong = models.ArtistSingSong.objects.filter(Q(artist__pk__exact=mainsong[0].artist.pk) & ~Q(song__pk__exact=mainsong[0].song.pk))[:10]
    
    return render(request, 'song.html',{
        'title': mainsong[0].song.title,
        'artist': maintitle[len(mainsong[0].song.title) + 1:],
        'mainsonginfo': mark_safe(json.dumps(mainsonginfo)),
        'likesong': likesong,
        'lyric':  mainsong[0].song.lyric
    })