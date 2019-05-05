from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^chat/(?P<room_name>[^/]+)/$', views.RoomListen),
    path('', views.IndexRoom),
    path('loadmore/', views.LoadMoreMessage),
    path('create/', views.Create_Room)
]