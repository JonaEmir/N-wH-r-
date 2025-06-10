from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def dama(request):
    return render(request, 'dama.html')

def caballero(request):
    return render(request, 'caballero.html')

def detalles(request):
    return render(request, 'detalles.html')
