from django.urls import path, include
from . import views
from .views import SongListView


urlpatterns = [
    #path('',views.Upload),
    path('song/',views.Song),
    path('song/add/',views.Add_song),
    path('artist/',views.Artist),
    path('artist/add/',views.Add_artist),
    path('',SongListView.as_view()),
] 
