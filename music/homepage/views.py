from django.shortcuts import render, redirect
from db import models
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
import json
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
        print(search_string)
        result_song = models.Song.objects.filter(title__icontains = search_string)
        #result_song = json.dumps(songs_to_json(result_song))
        for p in result_song:
            print (p.image.url)
        content= {
            'result_song': result_song,
            'search_string': search_string
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

    


