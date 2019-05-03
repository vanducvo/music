from django.shortcuts import render, redirect
from db import models
from django.http import HttpResponse
from django.views.generic.list import ListView

# Create your views here.

def Song(request):
        return render(request,'pages/song.html')

#Add song
def Add_song(request):
        song = models.Song()
        artistsingsong = models.ArtistSingSong()
       
        if (request.method == 'POST'):
                song.title = request.POST['title']
                song.image = request.FILES['image']
                song.genre = request.POST['genre']
                song.lyric = request.POST['lyric']
                song.audio = request.FILES['audio']
                song.producer = request.user
                song.save()

                artistsingsong.song = song
                if models.Artist.objects.filter(name = request.POST['artist']):
                        artistsingsong.artist = models.Artist.objects.get(name = request.POST['artist'])
                        artistsingsong.save()
                
                return redirect('/upload')

def Artist(request):
        return render(request,'pages/artist.html')

#Add artist
def Add_artist(request):
        artist = models.Artist()
        if (request.method =='POST'):
                artist.name = request.POST['name']
                artist.gender = request.POST['gender']
                artist.introduc = request.POST['introduc']
                artist.save()
                return redirect('/upload')

#View upload page
class SongListView(ListView):
        model = models.ArtistSingSong
        template_name = 'pages/upload.html'
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                return context