from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

salas = [
    {'id': 1, 'nome': 'Sala 1'},
    {'id': 2, 'nome': 'Sala 2'},
    {'id': 3, 'nome': 'Sala 3'},
]

def home(request):
    context = {'salas': salas}
    return render(request, 'base/home.html', context)

def sala(request, pk):
    sala = None

    for i in salas:
        if i['id'] == int(pk):
            sala = i

    context = {'sala': sala}

    return render(request, 'base/sala.html', context)
