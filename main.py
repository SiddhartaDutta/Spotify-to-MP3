"""
Main operation module.
"""

import os
from time import sleep
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import setup
from op_scripts.gen import clear_screen
import op_scripts.menus.program_op as program_op
import op_scripts.menus.program.auto_update as auto_update

if not os.path.isfile('.env'):
    print('[UPDATE] No user data detected.\n')
    setup.initialSetup()
else:
    print('[UPDATE] Starting Spotify to MP3...\n')

load_dotenv(override= True)

auth_manager = SpotifyClientCredentials(client_id=os.environ.get("SPOTIFYCLIENTID"), client_secret=os.environ.get("SPOTIFYCLIENTSECRET"))
sp = spotipy.Spotify(auth_manager=auth_manager)

# Launch Program
program_op.run(sp)

sleep(float(os.environ.get('MENUSLEEP')))
clear_screen()