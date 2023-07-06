import os
from dotenv import load_dotenv

import spotipy
import program

load_dotenv()

### Spotify Setup
sp = spotipy.Spotify(auth=os.environ.get("TOKEN"))

# RUN PROGRAM
program.run(sp)