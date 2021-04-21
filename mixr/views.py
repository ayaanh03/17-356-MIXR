from django.shortcuts import render
import random
import string

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {})
    
def joinPrivate(request):
    return render(request, 'joinPrivate.html', {})

def createRoom(request):
    context = {}
    context['randAlphaNum'] = generateAlphaNum()
    print(context['randAlphaNum'])
    return render(request, 'createRoom.html', context=context)

def hello(request):
    return HttpResponse('hello world.')

def generateAlphaNum():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str