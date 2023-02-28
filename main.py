from dotenv import load_dotenv
import os

# Downlo
import yt_dlp
import spotipy
from spotipy import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser

import spotifyScripts

load_dotenv()

### Spotify Setup

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

### Apple Music Setup


### Soundcloud Setup

#print(spotifyScripts.get_playlist_length(sp, '2T1a2GrAKZaAeBGw2WnBql'))

tempAMLength = 70
currentSpotifyLength = spotifyScripts.get_playlist_length(sp, '2T1a2GrAKZaAeBGw2WnBql')

if(tempAMLength != currentSpotifyLength):
        difference = currentSpotifyLength - tempAMLength
        print(difference)

        ids = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), '2T1a2GrAKZaAeBGw2WnBql')

        for index in range(tempAMLength, currentSpotifyLength):
        #for id in ids:
                trackID = ids[index]
                track = spotifyScripts.get_track_info(sp, trackID)
                print(track['name']+ ' - ' + track['artists'][0]['name'])

        #0CdFo515yc2vcintnGYG3b     <- single uzi playlist
        #2T1a2GrAKZaAeBGw2WnBql     <- 78 song uzi playlist