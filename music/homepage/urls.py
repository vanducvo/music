from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage,name = 'home'),
    path('signup/', views.SignUp),
    path('login/', views.Login),
    path('logout/', views.Logout, name = 'logout'),
    path('changepass/',views.ChangePass, name='changepass'),
]