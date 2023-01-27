from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
def home(request):
    return render(request, 'recipes/pages/home.html', context={
        "name": "Marvin"
    })

def sobre(request): 
    return HttpResponse("Sobre")

def contato(request): 
    return HttpResponse("Contato")
