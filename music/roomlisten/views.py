from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.template.defaultfilters import slugify
import json
import eyed3

# Create your views here.

@login_required
def RoomListen(request, room_name):
    room = models.RoomListen.objects.filter(name__exact=room_name)
    
    if list(room) == []:
            return render(request,'roomlisten/notify.html', {
                'infor': 'Phòng Không Tồn Tại'
            })
    room = room[0]
    playsist = models.SongInPlayist.objects.filter(playist__room__pk__exact=room.pk)
    songs = []
    i = 0
    for song in playsist:
        time = eyed3.load('/home/ducvovan/Source/main/music/music/' + song.song.audio.url).info.time_secs
        duration = str(int(time/60)) + ":" + str(int(time)%60).zfill(2)
        songname = song.song.title
        artists =  models.ArtistSingSong.objects.filter(song__pk__exact=song.song.pk)
        for artist in artists:
            songname =  songname + '-' + artist.artist.name

        songs.append({
            'track': i,
            'name': songname,
            'duration': duration,
            'file': song.song.audio.url
        })
        i = i + 1
    
    if room.user.username != request.user.username:
        if request.method == 'POST':
            password = request.POST['loginroompassword']
            if check_password(password, room.password):   
                return render(request, 'roomlisten/roomlisten.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)),
                     'username':mark_safe(json.dumps(request.user.username)),
                     'file': mark_safe(json.dumps(songs)),
                })
            else:
                return render(request,'roomlisten/notify.html',{
                    'infor': 'Mật Khẩu Không Đúng'
                })
        else:
            return render(request,'roomlisten/notify.html',{
                    'infor': 'Mật Khẩu Không Đúng'
                })

    return render(request, 'roomlisten/roomlisten.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username)),
        'file': mark_safe(json.dumps(songs)),
    })

@login_required
def IndexRoom(request):
    yourrooms = models.RoomListen.objects.filter(user__username__exact=request.user.username)
    otherrooms = models.RoomListen.objects.filter(~Q(user__username__exact=request.user.username))
    return render(request, 'roomlisten/index.html',{
        'yourroom':  yourrooms,
        'otherroom': otherrooms,
    })

@login_required
def LoadMoreMessage(request):
    align = int(request.GET['align'])
    time = int(request.GET['time'])
    room_name = request.GET['room']
    more = 10
    begin = align + time*more
    end =  begin + more
    messages =  models.Messenge.objects.filter(room__name__exact=room_name).order_by('-timestamp')[begin:end]
    content ={
        'messages': messages_to_json(messages),
    }

    return HttpResponse(json.dumps(content), content_type='aplication/json')

@login_required
def Create_Room(request):
    roomname = request.POST['roomname']
    roomtopic = request.POST['topic']
    roompassword = request.POST['password']
    room = models.RoomListen.objects.filter(name__exact=roomname)
    createuser = models.User.objects.filter(username__exact=request.user.username)[0]
    if(list(room) != []):
        return HttpResponse(status=417)

    nroom = models.RoomListen.objects.create(
        name = roomname,
        user = createuser,
        topic = roomtopic,
        password = make_password(roompassword)
    )

    models.Playist.objects.create(
        room = nroom,
        name = roomtopic,
        user = None
    )

    return HttpResponse(status=200)

@login_required
def SimpleSeach(request):
    if request.method == 'GET':
        subsongname = request.GET['song']
        songs = models.Song.objects.filter(title__icontains=subsongname)
        result = []
        for song in songs:
            art = ''
            artists =  models.ArtistSingSong.objects.filter(song__pk__exact=song.pk)
            for artist in artists:
                    art =  art + '-' + artist.artist.name
            
            result.append(song.title + art)

    return HttpResponse(json.dumps({'song': result}), content_type='aplication/json')


@login_required
def Infor(request):
    if request.method == 'GET':
        roomname = request.GET['name']
        room = models.RoomListen.objects.filter(name__exact=roomname)[0]
        playist = models.SongInPlayist.objects.filter(playist__room__name__exact=roomname)
        lplayist = []
        for song in playist:
            art = []
            artists =  models.ArtistSingSong.objects.filter(song__pk__exact=song.song.pk)

            for artist in artists:
                art.append(artist.artist.name)

            lplayist.append({
                'id': song.song.pk,
                'art': art,
                'title': song.song.title
            })

    return HttpResponse(json.dumps({
        'infor':{
            'topic': room.topic
        },
        'playist': lplayist,
    }), content_type='aplication/json')

@login_required
def manip_room(request):
    if request.method == 'POST':
        command =  request.POST['instruct']
        room = request.POST['name']
        if(command == 'addsong'):
            songartist = request.POST['song'].split('-')
            song = songartist[0]
            artist = songartist[1:]
            if len(artist) == 0:
                return HttpResponse("Không Tìm Thấy Bài Hát", status = 200)

            songs = models.ArtistSingSong.objects.filter(Q(song__title__exact=song) & Q(artist__name__exact=artist[0]))
            tsong = models.Song
            flag = True
            for isong in songs:
                flag = True
                for art in artist[1:]:
                    test = models.ArtistSingSong.objects.filter(Q(song__pk__exact=isong.pk) & Q(artist__name__exact=art))
                    if list(test) == []:
                        flag = False
                        break
                
                if flag:
                    tsong = isong.song
                    break
            
            if not flag:
                return HttpResponse(status=417)
            roomlisten = models.RoomListen.objects.filter(name__exact=room)[0]
            lplayist = models.Playist.objects.filter(room__name__exact=room)
            playist = models.Playist
            if list(lplayist) == []:
                playist = models.Playist(room = roomlisten, name= roomlisten.topic, user = None)
                playist.save()
            else:
                playist = lplayist[0]
            
            check = models.SongInPlayist.objects.filter(Q(playist__pk__exact=playist.pk) & Q(song__pk__exact=tsong.pk))
            if list(check) == []:
                addsong = models.SongInPlayist(playist = playist, song = tsong)
                addsong.save()
                return  HttpResponse(tsong.pk, status = 200)
            else:
                return HttpResponse("Không Tìm Thấy Bài Hát", status = 200)
        
        elif "delete-" in command:
            pk = int(command.split('-')[1])
            models.SongInPlayist.objects.filter(song__pk__exact=pk).delete()
         
    return HttpResponse(status=200)

@login_required
def editroom(request):
    if request.method == "POST":
        command = request.POST["command"]
        roomname = request.POST["roomname"]
        if command == "reinfo":
            room = models.RoomListen.objects.filter(name__exact=roomname)[0]
            topic = request.POST["topic"]
            password = request.POST["password"]
            if password != "Nhập Password Phòng":
                room.password = make_password(password)
            
            room.topic = topic
            room.save()
        elif command == "deleteroom":
            room = models.RoomListen.objects.filter(name__exact=roomname)[0]
            messageinroom = models.Messenge.objects.filter(room__pk__exact=room.pk)
            playistofroom = models.Playist.objects.filter(room__pk__exact=room.pk)[0]
            songinplayist = models.SongInPlayist.objects.filter(playist__pk__exact=playistofroom.pk)
            songinplayist.delete()
            playistofroom.delete()
            messageinroom.delete()
            room.delete()
            
        
    return HttpResponse("Thay Đổi Thành Công",status=200)

def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))

    return result

def message_to_json(message):
    return{
        'author': message.user.username,
        'message': message.content,
        'timestamp': str(message.timestamp)
    }

def rooms_to_json(rooms):
    result = []
    for room in rooms:
        result.append(room_to_json(room))
    
    return result

def room_to_json(room):
    return{
        'roomname': room.name,
        'user': room.user.username,
        'topic': room.topic,
    }