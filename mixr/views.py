from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
import random
import string
import pyrebase

# Spotify Auth Stuff
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
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
            return Room(request,form.cleaned_data['code'], 0)
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

    # From createRoom, host is true
    return redirect('/Room/'+context['code']+"/1")

@csrf_protect
def Room(request,code, host):
    # Int representing whether host or not

    t = db.child("Rooms").child(code).get().val()
    context = {}
    context['host'] = host
    context['code'] = code
    context['data'] = t
    try:
        context['playlist'] = t['playlist_id']
    except:
        return redirect('/joinPrivate/')
    try:
        query = request.POST['quantity']
        context['songs'] = {}
        # roomSongs should be pulled from database based on room code

        # dict which has URI:songName

        # pull curr songs from database
        roomSongs = db.child("Rooms").child(code).child("songs")
        # assuming roomSongs gets converted to a list of song uris:
        # print(roomSongs.keys())


        results = sp.search(q=query, limit=10, offset=0, type='track', market=None)
        # sp.playlist_replace_items(t['playlist_id'], context['roomSongs'].keys())

        #print(sp.current_user())
        for i, item in enumerate(results['tracks']['items']):
            context['songs'][str(i)] = item['name']
        return render(request,'Room.html',context)
    except:
        context['songs'] = {}
        return render(request, 'Room.html', context)


def search(request,code, query):
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

def getsongs(request,code, host):
    # host is 1 or 0 depending on true or false
    t = db.child("Rooms").child(code).get().val()
    songs = list(db.child("Rooms").child(code).child("songs").get().val().keys())

    results = []
    uris = []
    all_songs = {}
    for i, song in enumerate(songs):
        all_songs[(song,i)] = int(db.child("Rooms").child(code).child("songs").child(song).get().val())
    all_songs = {k: v for k, v in sorted(all_songs.items(), key=lambda item: item[1])[::-1]}

    final_songs = []
    for (song, i) in all_songs:
        results += [sp.track(song)['name']]
        uris += [sp.track(song)['uri']]
        final_songs.append(song)
    if host:
        sp.playlist_replace_items(t['playlist_id'], uris)
    final = {}
    for i in range(len(results)):
        final[results[i]] = final_songs[i]
    return render(request,"getsongs.html",{'results': final, 'code':code, 'host' : host})


def update_playlist(request, code, song, up_or_down, host):
    t = db.child("Rooms").child(code).get().val()
    songs = list(db.child("Rooms").child(code).child("songs").get().val().keys())
    current_count = int(db.child("Rooms").child(code).child("songs").child(song).get().val())
    if (up_or_down == "up"):
        current_count += 1
    else:
        current_count -= 1

    db.child("Rooms").child(code).child("songs").child(song).set(str(current_count))

    results = []
    uris = []
    all_songs = {}
    for i, song in enumerate(songs):
        all_songs[(song,i)] = int(db.child("Rooms").child(code).child("songs").child(song).get().val())
    all_songs = {k: v for k, v in sorted(all_songs.items(), key=lambda item: item[1])[::-1]}

    final_songs = []
    for (song, i) in all_songs:
        print(song)
        results += [sp.track(song)['name']]
        uris += [sp.track(song)['uri']]
        final_songs.append(song)
    if host:
        sp.playlist_replace_items(t['playlist_id'], uris)
    final = {}
    for i in range(len(results)):
        final[results[i]] = final_songs[i]
    return render(request, 'getsongs.html', {'results': final, 'code':code, 'host' : host})

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
