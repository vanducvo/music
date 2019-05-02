from django.shortcuts import render, redirect
from . import models
from django.http import HttpResponse
from django.views.generic.list import ListView

# Create your views here.

def Song(request):
        return render(request,'pages/song.html')

#Add song
def Add_song(request):
        song = models.Song()
        #artist1 = models.Artist(pk=3)
        if (request.method == 'POST'):
                song.name = request.POST['name']
                song.artist = request.POST['artist']
                song.genre = request.POST['genre']
                song.lyrics = request.POST['lyrics']
                song.audio = request.FILES['audio']
                song.save()
                return redirect('/upload')

def Artist(request):
        return render(request,'pages/artist.html')

#Add artist
def Add_artist(request):
        artist = models.Artist()
        if (request.method =='POST'):
                artist.name = request.POST['name']
                artist.age = request.POST['age']
                artist.introduc = request.POST['introduc']
                artist.save()
                return redirect('/upload')

#View upload page
class SongListView(ListView):
        model = models.Song
        template_name = 'pages/upload.html'
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                return context