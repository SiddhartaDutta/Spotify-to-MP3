import os
import dotenv
from dotenv import load_dotenv

import spotipy
import spotipy.util as util

import program

load_dotenv()

print('[UPDATE] Starting Spotify to MP3...')

# Token validity check
try:
    ### Spotify Setup
    sp = spotipy.Spotify(auth=os.environ.get("TOKEN"))

    testURN = 'spotify:artist:0gxyHStUsqpMadRV0Di1Qt'
    artist = sp.artist(testURN)

    print('[UPDATE] Token verified. Launching...\n')

except Exception:
    promptAns = str(input('[ERROR] Token has expired. The following process will open tab in your web browser and request authorization to create a new token.\nType \'Y\' to proceed or \'N\' to cancel: '))
    if(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):

        print('[UPDATE] Re-generating token. This process may take several minutes...')
        try:
            os.environ['TOKEN'] = util.prompt_for_user_token(username= os.environ.get("USERNAME"),
                                                            scope= "user-library-read",
                                                            client_id= os.environ.get("CLIENTID"),
                                                            client_secret= os.environ.get("CLIENTSECRET"),
                                                            redirect_uri= "http://localhost:1234/")
            dotenv.set_key(dotenv.find_dotenv(), "TOKEN", os.environ['TOKEN'])
        except:
            print('[UPDATE] Update cancelled. \'.env\' file missing. Please re-install Spotify to MP3.')
            exit()

        print('[UPDATE] Token verified. Launching...\n')

    else:
        print('[UPDATE] Update cancelled. To use Spotify to MP3 in the future, please update.')
        exit()

    ### Spotify Setup
    sp = spotipy.Spotify(auth=os.environ.get("TOKEN"))

# Launch Program
program.run(sp)