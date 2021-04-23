import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

'''
Script to get search results based on query
'''

scope = 'user-top-read'

os.environ["SPOTIPY_CLIENT_ID"]='3833b3fffe714b61acb9e438b90dd25a'
os.environ["SPOTIPY_CLIENT_SECRET"]='5f0e93275b254646b6ec8f277e2f7a6a'
os.environ["SPOTIPY_REDIRECT_URI"]='http://127.0.0.1:3000/mixr/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# q is the query (eg. q='hi' would give you Spotify search results for 'hi')
results = sp.search(q='', limit=10, offset=0, type='track', market=None)

# Prints out the tracks 
for i, item in enumerate(results['tracks']['items']):
    print(i, item['name'])