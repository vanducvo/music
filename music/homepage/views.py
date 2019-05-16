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

def Contact(request):
    return render(request,'homepage/contact.html')

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

def Error(request):
    return(request,'homepage/404.html')

def Search(request):
        if request.is_ajax():
            print('is ajax')
            if(request.method == 'POST'):
                search_string =  request.POST['search_string']
                print (search_string)
                result_song = models.ArtistSingSong.objects.filter(song__title__icontains = search_string)
                result_artist = models.ArtistSingSong.objects.filter(artist__name__icontains = search_string)
                #for s in result_song:
                #    print(s.song.title)
                #for a in result_artist:
                #tháng    print(a.artist.name)
                return HttpResponse(json.dumps(return_to_json(result_song,result_artist)), content_type='aplication/json')
        else:
            print('is not ajax')
            if(request.method == 'POST'):
                search_string =  request.POST['searchtext']
                result_song = models.ArtistSingSong.objects.filter(song__title__icontains = search_string)
                artist = models.ArtistSingSong.objects.filter(artist__name__icontains = search_string)
                print (search_string)
                #with connection.cursor() as cursor:
                #    cursor.execute("select title,image,audio,lyric,genre,name from dbmusic.db_song inner join dbmusic.db_artistsingsong on dbmusic.db_song.id = dbmusic.db_artistsingsong.song_id inner join dbmusic.db_artist on dbmusic.db_artistsingsong.artist_id=dbmusic.db_artist.id where dbmusic.db_song.title like '%" + search_string + "%'")
                #    result_song =  namedtuplefetchall(cursor)
                #result_song = json.dumps(songs_to_json(result_song))      
                s_artist = []
                result_artist = []
                for p in artist:
                    s_artist.append(p.artist)
                count_ar = 0
                s_artist = set(s_artist)
                for j in s_artist:
                    #print(j)
                    count_ar += 1 
                #print(count_ar)
                content= {
                    'result_song': result_song,
                    'search_string': search_string,
                    'artist': artist,
                    'count_ar': count_ar,
                    's_artist' : s_artist,
                }
                # result_artist = models.Artist.objects.get(name__icontains = search_string)
                #return HttpResponse(json.dumps(songs_to_json(result_song)), content_type='aplication/json')
                return render(request,'homepage/search.html' ,{'content':content})
            else:    
                return render(request,'homepage/homepage.html')

def return_to_json(objects1, objects2):
    result =[]
    result_songs_a=[]
    result_artist=[]
    result_set_ar=[]
    result_songs=[]
    set_ar=[]
    for s in objects1:
        result_songs.append(song_to_json(s))
    for a in objects2:
        set_ar.append(a.artist)
    set_ar = set(set_ar)
    for a in set_ar:
        result_set_ar.append(set_ar_to_json(a))
    for s in objects2:
        result_songs_a.append(song_to_json(s))
    for a in objects2:
        result_artist.append(artist_to_json(a))
    
    result.append(result_songs)
    result.append(result_set_ar)
    result.append(result_songs_a)
    result.append(result_artist)
    return result
def artist_to_json(obj):
    return {
        'id' : obj.artist.id,
        'name': obj.artist.name,
        'introduc': obj.artist.introduc
    }
def set_ar_to_json(obj):
    return{
        'id' : obj.id,
        'name': obj.name,
        'introduc': obj.introduc
    }
def songs_to_json(objects):
    result =[]
    for o in objects:
        result.append(song_to_json(o))
    return result

def song_to_json(obj):
    return {
        'title': obj.song.title,
        'id': obj.song.id,
        'image': obj.song.image.url,
        'audio': obj.song.audio.url,
        'lyric': obj.song.lyric,
        'genre': obj.song.genre,
        'name' : obj.artist.name,
    }
def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


    


