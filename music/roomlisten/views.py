from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from db import models
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.template.defaultfilters import slugify
import json

# Create your views here.

@login_required
def RoomListen(request, room_name):
    room = models.RoomListen.objects.filter(name__exact=room_name)
    if list(room) == []:
            return render(request,'roomlisten/notify.html', {
                infor: 'Phòng Không Tồn Tại'
            })
    
    room = room[0]
    if room.user.username != request.user.username:
        if request.method == 'POST':
            password = request.POST['loginroompassword']
            if check_password(password, room.password):   
                return render(request, 'roomlisten/roomlisten.html', {
                    'room_name_json': mark_safe(json.dumps(room_name)),
                     'username':mark_safe(json.dumps(request.user.username)),
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

    models.RoomListen.objects.create(
        name = roomname,
        user = createuser,
        topic = roomtopic,
        password = make_password(roompassword)
    )
    return HttpResponse(status=200)

@login_required
def SimpleSeach(request):
    if request.method == 'GET':
        subsongname = request.GET['song']
        songs = models.Song.objects.filter(title__icontains=subsongname)
        result = []
        for song in songs:
            result.append(song.title)

    return HttpResponse(json.dumps({'song': result}), content_type='aplication/json')


@login_required
def Infor(request):
    if request.method == 'GET':
        roomname = request.GET['name']
        room = models.RoomListen.objects.filter(name__exact=roomname)[0]
    
    return HttpResponse(json.dumps({'infor':{'topic': room.topic}}), content_type='aplication/json')


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