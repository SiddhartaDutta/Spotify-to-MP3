import os
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import op_scripts.menus.program_op as program_op
import op_scripts.menus.program.auto_update as auto_update

load_dotenv(override= True)

print('[UPDATE] Starting Spotify to MP3...\n')

auth_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIFYCLIENTID"), client_secret=os.environ.get("SPOTIFYCLIENTSECRET"))
sp = spotipy.Spotify(auth_manager=auth_manager)

# Launch Program
program_op.run(sp)
