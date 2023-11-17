import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import program

load_dotenv()

print('[UPDATE] Starting Spotify to MP3...\n')

auth_manager = SpotifyClientCredentials(client_id=os.environ.get("CLIENTID"), client_secret=os.environ.get("CLIENTSECRET"))
sp = spotipy.Spotify(auth_manager=auth_manager)

# Launch Program
program.run(sp)
