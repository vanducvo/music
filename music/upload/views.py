from django.shortcuts import render, redirect
from db import models
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib import messages

# Create your views here.

class ArtistListView(ListView):
        model = models.Artist
        template_name = 'pages/song.html'
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                return context

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
                else :
                        messages.warning(request, 'Ca Sĩ Không Hợp Lệ',extra_tags='safe')
                        return redirect('/upload/error.html')

def Artist(request):
        return render(request,'pages/artist.html')

#Add artist
def Add_artist(request):
        artist = models.Artist()
        if (request.method =='POST'):
                artist.name = request.POST['name']
                artist.gender = request.POST['gender']
                artist.introduc = request.POST['introduc']
                if models.Artist.objects.filter(name=artist.name):
                        messages.warning(request,'Ca Sĩ Đã Tồn Tại',extra_tags='safe')
                        return redirect('/upload/error.html')
                else:
                        artist.save()
                        return redirect('/upload')
        else : 
                return redirect('/upload/error.html')
#View upload page
class SongListView(ListView):
        model = models.ArtistSingSong
        template_name = 'pages/upload.html'
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                return context

# def Edit(request, pk):
#         model = models.Artist
#         return render(request,'pages/edit.html', {'pk': pk})
class EditListView(ListView):
        model = models.Artist
        template_name = 'pages/edit.html'
        def get_context_data(self,**kwargs):
                context = super().get_context_data(**kwargs)
                return context

def X(request):
        obj = models.Song.objects.filter(id__exact=int(request.POST['pk']))[0]
        obj.title = request.POST['title']
        obj.image = request.FILES['image']
        obj.genre = request.POST['genre']
        obj.lyric = request.POST['lyric']
        obj.audio = request.FILES['audio']
        
        artistsingsong = models.ArtistSingSong.objects.filter(song = obj)[0]
        if models.Artist.objects.filter(name = request.POST['artist']):
                artistsingsong.artist = models.Artist.objects.get(name = request.POST['artist'])
                obj.save()
                artistsingsong.save()
        else :
                messages.warning(request,'Ca Sĩ Không Tồn Tại', extra_tags='safe')
                return redirect('/upload/error.html')
        return redirect('/upload')

def Delete(request, pk):
        obj = models.Song.objects.get(pk=pk)
        obj.delete()
        return redirect('/upload')

def Error(request):
        return render(request,'pages/error.html')