from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

# Create your views here.

@login_required
def RoomListen(request, room_name):
    return render(request, 'roomlisten/roomlisten.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

@login_required
def IndexRoom(request):
    return render(request, 'roomlisten/index.html',{})