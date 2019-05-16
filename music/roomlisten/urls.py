from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chat/(?P<room_name>[^/]+)/$', views.RoomListen),
    path('', views.IndexRoom, name = 'roomlisten'),
    path('loadmore/', views.LoadMoreMessage),
    path('create/', views.Create_Room),
    path('simplesearch/', views.SimpleSeach),
    path('inforoom/', views.Infor),
    path('maniproom/', views.manip_room),
    path('editroom/', views.editroom),
]