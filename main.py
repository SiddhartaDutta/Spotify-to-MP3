import os
from dotenv import load_dotenv

import spotipy
from spotipy import SpotifyOAuth

import program

load_dotenv()

### Spotify Setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

# RUN PROGRAM
program.run(sp)