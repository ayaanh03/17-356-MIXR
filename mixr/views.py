from django.shortcuts import render

import random
import string
import pyrebase

# Create your views here.
config = {
  "apiKey": "AIzaSyDOAMIg3T_NToCDwqhNRTXKWXCuaRn6O9Q",
  "authDomain": "mixr-17-356.firebaseapp.com",
  "databaseURL": "https://mixr-17-356-default-rtdb.firebaseio.com",
  "projectId": "mixr-17-356",
  "storageBucket": "mixr-17-356.appspot.com",
  "messagingSenderId": "1097388094664",
  "appId": "1:1097388094664:web:254cf663cf38fc773d21fd",
  "measurementId": "G-V5QVSSZ5DK"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
db=firebase.database()

def mixr(request):
    # print(database.get().val())
    return render(request,"Home.html")

# Create your views here.
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html', {})
    
def joinPrivate(request):
    return render(request, 'joinPrivate.html', {})

def createRoom(request):
    context = {}
    context['code'] = generateAlphaNum()
    # checking for used Room code and generating a new one in case it was used. 
    while db.child("Rooms").child(context['code']).get().val() != None :
        context['code'] = generateAlphaNum()
    db.child("Rooms").update({context['code'] : "bruh"})
    return render(request, 'createRoom.html', context=context)

def hello(request):
    return HttpResponse('hello world.')

def generateAlphaNum():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str




