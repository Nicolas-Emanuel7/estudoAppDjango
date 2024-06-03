from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from django.contrib import messages
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        print(email, password)

        try:
            user = User.objects.get(email = email)
        except:
            messages.error(request, 'Usuário não encontrado')
            return redirect('login')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha incorretos')
            return redirect('login')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Erro ao criar usuário')
        
    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    salas = Room.objects.filter( #Isso faz uma busca por nome do topico, nome da sala e descrição da sala
        Q(topic__name__icontains=q) | #Isso faz uma busca por nome do topico
        Q(name__icontains=q) | #Isso faz uma busca por nome da sala
        Q(description__icontains=q) #Isso faz uma busca por descrição da sala
        )

    topicos = Topic.objects.all()[0:5]

    sala_count = salas.count()

    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'salas': salas, 'topicos': topicos, 'sala_count': sala_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)

def sala(request, pk):
    sala = Room.objects.get(id=pk)
    sala_messages = sala.message_set.all()
    participants = sala.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = sala,
            body = request.POST.get('body')
        )

        sala.participants.add(request.user)
        return redirect('sala', pk=sala.id)

    context = {'sala': sala, 'sala_messages': sala_messages, 'participants': participants}

    return render(request, 'base/sala.html', context)

def user_profile(request, pk):
    user = User.objects.get(id=pk)
    salas = user.room_set.all()
    room_messages = user.message_set.all()
    topicos = Topic.objects.all()

    context = {'user': user, 'salas': salas , 'room_messages': room_messages, 'topicos': topicos}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def create_sala(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        print(request.POST)
        
        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
       

    context = {'form': form, 'topics': topics}
    return render(request, 'base/sala_form.html', context)

@login_required(login_url='login')
def update_sala(request, pk):
    sala = Room.objects.get(id=pk)

    form = RoomForm(instance=sala)
    topics = Topic.objects.all()

    if request.user != sala.host:
        return HttpResponse('Você não tem permissão para editar essa sala')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        sala.name = request.POST.get('name')
        sala.description = request.POST.get('description')
        sala.topic = topic
        sala.save()

        return redirect('home')

    context = {'form': form, 'topics': topics, 'sala': sala}
    return render(request, 'base/sala_form.html', context)

@login_required(login_url='login')
def delete_sala(request, pk):
    sala = Room.objects.get(id=pk)

    if request.user != sala.host:
        return HttpResponse('Você não tem permissão para editar essa sala')
    
    if request.method == 'POST':
        sala.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': sala})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Você não tem permissão para apagar essa mensagem')
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})

@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})

def topics_page(request):
    q = request.GET.get('q') if request.GET.get('q')!=None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'base/topics.html', {'topics': topics})

def activity_page(request):
    room_messages = Message.objects.all()

    return render(request, 'base/activity.html', {'room_messages': room_messages})