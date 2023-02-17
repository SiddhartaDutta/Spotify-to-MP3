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

# taylor_uri = 'spotify:artist:06HL4z0CvFAxyc27GXpf02'
# results = sp.artist_albums(taylor_uri, album_type='album')

# results1 = sp.current_user_playlists(limit=50)

# for i, item in enumerate(results1['items']):
#     print("%d %s" % (i, item['name']))

def get_playlist_ids(username,playlist_id):
    r = sp.user_playlist_tracks(username,playlist_id)
    t = r['items']
    ids = []
    while r['next']:
        r = sp.next(r)
        t.extend(r['items'])
    for s in t: ids.append(s["track"]["id"])
    return ids

def get_playlist_length(playlistId):
    """
    Takes a Spotify playlist ID and returns the playlist's length.
    """

    playlist = sp.playlist_items(playlist_id=playlistId, offset=0, fields='items.track.id,total', additional_types=['track'])
    return playlist['total']
    
    # offset = 0
    # while offset != -1:
    #     response = sp.playlist_items(playlist_id, offset=0, fields='items.track.id,total', additional_types=['track'])

    #     if len(response['items']) == 0:
    #         break

    #     print(response['items'])
    #     offset = offset + len(response['items'])
    #     print(offset, "/", response['total'])

    #     if offset == response['total']:
    #         offset = -1

        #0CdFo515yc2vcintnGYG3b     <- single uzi playlist
        #2T1a2GrAKZaAeBGw2WnBql     <- 78 song uzi playlist

print(get_playlist_length('0CdFo515yc2vcintnGYG3b'))