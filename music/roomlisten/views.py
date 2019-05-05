from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from db import models
import json

# Create your views here.

@login_required
def RoomListen(request, room_name):
    return render(request, 'roomlisten/roomlisten.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username':mark_safe(json.dumps(request.user.username)),
    })

@login_required
def IndexRoom(request):
    return render(request, 'roomlisten/index.html',{})

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