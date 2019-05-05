from django.urls import path, include, re_path
from django.conf.urls import url
from . import views
from .views import SongListView, ArtistListView, EditListView


urlpatterns = [
    path('song/',ArtistListView.as_view()),
    path('song/add/',views.Add_song),
    path('artist/',views.Artist),
    path('artist/add/',views.Add_artist),
    path('',SongListView.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$',EditListView.as_view(), name='edit_song'),
    re_path(r'^delete/(?P<pk>\d+)/$',views.Delete, name='delete_song'),
    path('edit/x/',views.X),
    path('error.html',views.Error),
] 
