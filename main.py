import yt_dlp
import spotipy
#from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import SpotifyOAuth
from dotenv import load_dotenv
import os
import json
import webbrowser

load_dotenv()

# auth_manager = SpotifyClientCredentials(client_id=os.environ.get("CLIENTID"), client_secret=os.environ.get("CLIENTSECRET"))
# sp = spotipy.Spotify(auth_manager=auth_manager, scope='playlist-read-private')


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'

results = sp.artist_albums(taylor_uri, album_type='album')
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])