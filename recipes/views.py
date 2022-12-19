from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'recipes/home.html', status=200, context={'name': 'Queiroz Santana'})


def contato(request):
    return HttpResponse('CONTACTO')


def sobre(request):
    return HttpResponse('SOBRE')