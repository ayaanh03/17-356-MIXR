from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import random
import string
import pyrebase

# Spotify Auth Stuff
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

scope = 'user-top-read user-library-read playlist-modify-private'

# os.environ["SPOTIPY_CLIENT_ID"]='3833b3fffe714b61acb9e438b90dd25a'
# os.environ["SPOTIPY_CLIENT_SECRET"]='5f0e93275b254646b6ec8f277e2f7a6a'
# os.environ["SPOTIPY_REDIRECT_URI"]='http://127.0.0.1:3000/mixr/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,client_id = '3833b3fffe714b61acb9e438b90dd25a',client_secret= '5f0e93275b254646b6ec8f277e2f7a6a',redirect_uri= 'http://127.0.0.1:3000/mixr/'))
print("Scope",scope)
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
from .forms import JoinForm
def home(request):
    return render(request, 'home.html', {})

def joinPrivate(request):
    if request.method == 'POST':
        form = JoinForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return Room(request,form.cleaned_data['code'])
    return render(request, 'joinPrivate.html', {})

def createRoom(request):
    context = {}
    context['code'] = generateAlphaNum()
    # checking for used Room code and generating a new one in case it was used.
    while db.child("Rooms").child(context['code']).get().val() != None :
        context['code'] = generateAlphaNum()

    # Associate a playlist with the room (name of playlist is the room code)
    playlist = sp.user_playlist_create(sp.current_user()['id'], context['code'], public=False, 
                                         collaborative=True, description='17356 bops')
    db.child("Rooms").update({context['code'] : {'playlist_id':playlist['id']}})
    
    return Room(request, context['code'])

@csrf_protect
def Room(request,code):
    t = db.child("Rooms").child(code).get().val()
    context = {}
    context['code'] = code
    context['data'] = t
    try:
        query = request.POST['quantity']
    except:
        query = "a"
    context['songs'] = {}
    # roomSongs should be pulled from database based on room code
    # dict which has URI:songName
    context['roomSongs'] = {'spotify:track:3bYRjffJlvaDWqeUqEjaUU': 'SDGAF', 
                 'spotify:track:4FGpxdVFIhIVzRq8X64a1I': 'Sdgaf', 
                 'spotify:track:0iCOMK0czjVWfgFeiqkvQT': 'Sunday 3pm - Reconstructed', 
                 'spotify:track:7ugDr4fb1KWoLUGgJzoatK': 'Sunday 3pm - Kenji Club Remix', 
                 'spotify:track:7xS6EPi3KX8PcxuNdOPxQ5': 'Miracle - Signfield Mix'}
    results = sp.search(q=query, limit=10, offset=0, type='track', market=None)
    print(sp.current_user())
    for i, item in enumerate(results['tracks']['items']):
        context['songs'][str(i)] = item['name']
    return render(request,'Room.html',context)



def search(request, query):
    results = sp.search(q=query, limit=10, offset=0, type='track', market=None)
    songs = {}
    test = {}
    for i, item in enumerate(results['tracks']['items']):

        songs[str(i)] = item['name']+" "+item['uri']
        test[item['uri'].split(":")[2]] = item['name']
    print(test)
    return render(request,'search.html',{'songs': test,'code': code})


def addsong(request, code, song):
    db.child("Rooms").child(code).child("songs").child(song).set("0")
    return render(request,'search.html')

def getsongs(request,code):
    songs = list(db.child("Rooms").child(code).child("songs").get().val().keys())
    results = []
    for song in songs:
        results += [sp.track(song)['name']]
    # print(results)
    return render(request,"getsongs.html",{'results': results})

def Playlist(request):
    # Hardcoded list of songs uris
    song_dict = {'spotify:track:3bYRjffJlvaDWqeUqEjaUU': 'SDGAF', 
                 'spotify:track:4FGpxdVFIhIVzRq8X64a1I': 'Sdgaf', 
                 'spotify:track:0iCOMK0czjVWfgFeiqkvQT': 'Sunday 3pm - Reconstructed', 
                 'spotify:track:7ugDr4fb1KWoLUGgJzoatK': 'Sunday 3pm - Kenji Club Remix', 
                 'spotify:track:7xS6EPi3KX8PcxuNdOPxQ5': 'Miracle - Signfield Mix'}
    song_uris = song_dict.keys()
    song_list = song_dict.values()
    playlist = sp.user_playlist_create(sp.current_user()['id'], '17356_playlist', public=False, 
                                         collaborative=False, description='17356 bops')
    sp.playlist_add_items(playlist['id'], song_uris, position=None)
    return render(request, 'Playlist.html', {'songs': song_list})


def hello(request):
    return HttpResponse('hello world.')

def generateAlphaNum():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(4))
    return result_str
