from django.urls import path
from . import views

urlpatterns = [
    path('', views.Homepage),
    path('signup/', views.SignUp),
    path('login/', views.Login),
    path('logout/', views.Logout),
]