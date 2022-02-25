from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate ,login , logout
from .models import Room , Message
from django.core.files.storage import FileSystemStorage
# Create your views here.
def index(request):
    rooms = Room.objects.filter(users = request.user)
    users = User.objects.all().exclude(username =request.user.username )
    # create = User.objects.all().exclude()
    return render(request, 'channel.html' , {
        'rooms':rooms,
        'users':users
    })
def roomview(request, room_name):
    room = Room.objects.get(rid =room_name )
    if request.user in room.users.all():
        rooms = Room.objects.filter(users = request.user).order_by('-lastdate')
        users = User.objects.all().exclude(username =request.user.username )
        messages = Message.objects.filter(room= room ) 
        return render(request, 'channels.html', {
            'room_name': room_name,
            'room': room,
            'rooms':rooms,
            'users':users,
            'messages':messages,
        })
    else:
        return HttpResponse("bu odaya girmeye yetkin/hakkın yok")
def loginview(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username= username , password = password)
        if user:
            login(request,user)
            return HttpResponse(f"logged as {username} ")
        return HttpResponse("hata")
    else:
        return render(request,"login.html")
import os
def getfiletype(msg):
    name, extension = os.path.splitext(msg.mfile.name)
    if extension == '.jpg':
        return 'ok'
from django.http import JsonResponse
import json
def imgpost(request):
    myfile = request.FILES['file']
    roomname = request.POST['roomname']
    fs = FileSystemStorage()
    saved = fs.save(myfile.name, myfile)
    room = Room.objects.get(rid = roomname)
    msg =  Message.objects.create(user = request.user ,room =  room ,mtype = "file" , mfile = saved ,content = myfile.name)
    return JsonResponse({
        '1':myfile.name,
        '2': msg.mfile.url,
        '3' :getfiletype(msg)
    })

def get_room(request ,id ):
    targetuser = User.objects.get(pk = id)
    room = Room.objects.filter(users = targetuser).filter(users = request.user)
    try:
        room= room[0]
    except:
        room = Room.objects.create()
        room.users.add(request.user)
        room.users.add(targetuser)
        print(room)
        return redirect("/chat/"+room.rid )
    return redirect("/chat/"+ room.rid)


    