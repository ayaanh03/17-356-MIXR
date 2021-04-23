import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
scope = 'user-top-read'

os.environ["SPOTIPY_CLIENT_ID"]='3833b3fffe714b61acb9e438b90dd25a'
os.environ["SPOTIPY_CLIENT_SECRET"]='5f0e93275b254646b6ec8f277e2f7a6a'
os.environ["SPOTIPY_REDIRECT_URI"]='http://127.0.0.1:3000/mixr/'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


for sp_range in ['short_term', 'medium_term', 'long_term']:
    print("range:", sp_range)

    results = sp.current_user_top_artists(time_range=sp_range, limit=50)

    for i, item in enumerate(results['items']):
        print(i, item['name'])
    print()