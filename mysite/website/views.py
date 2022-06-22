from ast import Delete
from email import message
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from multiprocessing import context, reduction
from pydoc_data.topics import topics
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Room, Topic
from .form import RoomForm

# rooms = [
#     {'id' : '1', 'name': 'Mas Zidane'},
#     {'id' : '2', 'name': 'Mas Zidane aye'},
#     {'id' : '3', 'name': 'Mas Zidane oke'},
# ]

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username or Password does not exist')

    context = {}
    return render(request, 'home/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('index')


def index(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q)
    )

    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'home/index.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    return render(request, 'home/room.html')

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form':form}
    return render(request, 'home/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('index')

    context = {'form' : form}
    return render(request, 'home/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.method == 'POST':
        room.delete()
        return redirect('index')

    return render(request, 'home/delete.html', {'obj':room})