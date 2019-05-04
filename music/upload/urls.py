from django.urls import path, include, re_path
from django.conf.urls import url
from . import views
from .views import SongListView


urlpatterns = [
    #path('',views.Upload),
    path('song/',views.Song),
    path('song/add/',views.Add_song),
    path('artist/',views.Artist),
    path('artist/add/',views.Add_artist),
    path('',SongListView.as_view()),
    re_path(r'^edit/(?P<pk>\d+)/$',views.Edit, name='edit_song'),
    re_path(r'^delete/(?P<pk>\d+)/$',views.Delete, name='delete_song'),
    path('edit/x/',views.X)
] 
