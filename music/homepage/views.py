from django.shortcuts import render, redirect
from db import models
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import json
from django.db import connection
from collections import namedtuple
# Create your views here.

def Homepage(request):
    return render(request,'homepage/homepage.html')


def SignUp(request):
    user = models.User()
    if(request.method == 'POST'):
        user.username = request.POST['username']
        user.email = request.POST['email']
        checkuser = list(models.User.objects.filter(username__exact=user.username))
        if checkuser != []:
            return HttpResponse(status=417)

        checkuser = list(models.User.objects.filter(email__exact=user.email))
        if checkuser != []:
            return HttpResponse(status=418)
        
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.gender = request.POST['gender']
        if request.POST['role']== 'user':
            user.is_staff = False
        elif request.POST['role']== 'publisher':
            user.is_staff = True

        user.set_password(request.POST['password'])
        user.save()
        return HttpResponse(status=200)
    
    
def Login(request):
    if request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        
        if user is not None:
            login(request, user)

    return redirect('/')

def Logout(request):
    logout(request)
    return redirect('/')

    
def ChangePass(request):
    User=models.User
    if(request.method == 'POST'):
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            user.set_password(request.POST['newpassword'])
            user.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=417)
def Search(request):
    if(request.method == 'POST'):
        search_string =  request.POST['searchtext']
        result_song = models.ArtistSingSong.objects.filter(song__title__icontains = search_string)
        artist = models.ArtistSingSong.objects.filter(artist__name__icontains = search_string)
        print (search_string)
        #with connection.cursor() as cursor:
        #    cursor.execute("select title,image,audio,lyric,genre,name from dbmusic.db_song inner join dbmusic.db_artistsingsong on dbmusic.db_song.id = dbmusic.db_artistsingsong.song_id inner join dbmusic.db_artist on dbmusic.db_artistsingsong.artist_id=dbmusic.db_artist.id where dbmusic.db_song.title like '%" + search_string + "%'")
        #    result_song =  namedtuplefetchall(cursor)
        #result_song = json.dumps(songs_to_json(result_song))      
        t_artist = []
        result_artist = []
        for p in artist:
            t_artist.append(p.artist)
        count_ar = 0
        t_artist = set(t_artist)
        for j in t_artist:
            #print(j)
            count_ar += 1 
        #print(count_ar)
        for p in artist:
            for k in t_artist:
                if p.artist == k:
                    result_artist.append(p)
                    break
        content= {
            'result_song': result_song,
            'search_string': search_string,
            'result_artist': result_artist,
            'count_ar': count_ar,
            't_artist' : t_artist
        }
       # result_artist = models.Artist.objects.get(name__icontains = search_string)
        #return HttpResponse(json.dumps(songs_to_json(result_song)), content_type='aplication/json')
        return render(request,'homepage/search.html' ,{'content':content})
    else:    
        return render(request,'homepage/homepage.html')

def songs_to_json(songs):
    result =[]
    for song in songs:
        result.append(song_to_json(song))

    return result

def song_to_json(song):
    return {
        'title': song.title,
        'image': song.image.url,
        'audio': song.audio.url,
        'lyric': song.lyric,
        'genre': song.genre,
    }
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


    


