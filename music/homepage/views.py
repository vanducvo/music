from django.shortcuts import render, redirect
from db import models
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
# Create your views here.

def Homepage(request):
    return render(request,'homepage/homepage.html')


def SignUp(request):
    user = models.User()
    if(request.method == 'POST'):
        user.username = request.POST['username']
        user.email = request.POST['email']
        checkuser = list(models.User.objects.filter(username__exact=user.username))
        if checkuser != []:
            return HttpResponse(status=417)

        checkuser = list(models.User.objects.filter(email__exact=user.email))
        if checkuser != []:
            return HttpResponse(status=418)
        
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.gender = request.POST['gender']
        if request.POST['role']== 'user':
            user.is_staff = False
        elif request.POST['role']== 'publisher':
            user.is_staff = True

        user.set_password(request.POST['password'])
        user.save()
        return HttpResponse(status=200)
    
    
def Login(request):
    if request.method == 'POST':
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        
        if user is not None:
            login(request, user)

    return redirect('/')

def Logout(request):
    logout(request)
    return redirect('/')


    


