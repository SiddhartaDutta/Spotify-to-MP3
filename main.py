from dotenv import load_dotenv
import os
import requests

# Downloaded
import yt_dlp
from yt_dlp import YoutubeDL
import spotipy
from spotipy import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser

from pprint import pprint

import spotifyScripts
import osScripts

load_dotenv()

### Spotify Setup

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

### Apple Music Setup


### Soundcloud Setup

tempAMLength = 70
currentSpotifyLength = spotifyScripts.get_playlist_length(sp, '2T1a2GrAKZaAeBGw2WnBql')

if(tempAMLength != currentSpotifyLength):
        #print(currentSpotifyLength - tempAMLength)

        ids = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), '2T1a2GrAKZaAeBGw2WnBql')
        
        # image extraction test code
        #pprint(spotifyScripts.get_album_cover_url(sp, ids[0]))
        osScripts.download_img('Eternal Atake', spotifyScripts.get_album_cover_url(sp, ids[0]))

        # album name extraction test code
        albums = spotifyScripts.get_albums_from_ids(sp, tempAMLength, currentSpotifyLength, ids)
        #pprint(albums)

        # album directory creation test code
        #osScripts.create_album_dir(albums)

        # print songs

        ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                }],
                'postprocessor_args': [
                        '-ar', '16000'
                ],
                'prefer_ffmpeg': True,
                'keepvideo': False
        }

        for id in ids:
                track = spotifyScripts.get_track_info(sp, id)
                pprint(track['name'] + ' Official Audio')
                searchString = track['name'] + ' Official Audio'

                with YoutubeDL(ydl_opts) as ydl:
                        video = str(ydl.extract_info(f"ytsearch:{searchString}", download= False)['entries'][0]['webpage_url'])
                        pprint(video)

                        ydl.download([video])

                        break

        # with YoutubeDL(ydl_opts) as ydl:
        #         ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])


        # song download test code
        
        

        #0CdFo515yc2vcintnGYG3b     <- single uzi playlist
        #2T1a2GrAKZaAeBGw2WnBql     <- 78 song uzi playlist