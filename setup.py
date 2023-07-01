from time import sleep

from dotenv import load_dotenv

import spotipy
from spotipy import SpotifyOAuth

import spotifyScripts

load_dotenv()

def initialSetup():

    print("The following will setup Spotify-to-MP3 for you.")
    sleep(0.5)
    print("Please enter the information as requested...")
    sleep(0.5)

    username = str(input("Please enter your Spotify username: "))
    clientID = str(input("Please input your generated Client ID: "))
    clientSecret = str(input("Please input your generated Client Secret: "))

    # Get number of playlists to be added
    numOfPlaylists = None
    while numOfPlaylists == None:
        try:
            numOfPlaylists = int(input("Please input the number of Spotify playlists you wish to update: "))
        except:
            print("[ERROR] Invalid input. Please input a number.")

    # Get playlist IDs
    playlistIDs = []
    while(len(playlistIDs)) < numOfPlaylists:
        playlistIDs.append(str(input('Please input a playlist ID for playlist #' + str(len(playlistIDs)+1) + ': ')))

    # Get playlist downloaded
    playlistLengths = []
    while len(playlistLengths) < numOfPlaylists:
        try:
            playlistLengths.append(int(input('Please enter the current number of downloaded songs for playlist with ID ' + playlistIDs[len(playlistLengths)] + ': ')))
        except:
            print("[ERROR] Invalid input. Please input a number (input '0' for non-downloaded playlists).")

    # Format playlist arrays for env file addition
    playlistLengthStr = playlistIDStr = '['
    for Length, ID in zip(playlistLengths, playlistIDs):

        # Process length
        tempStr = str(Length)
        tempStr = '"' + tempStr + '",'
        playlistLengthStr += tempStr

        # Process ID
        tempStr = str(ID)
        tempStr = '"' + tempStr + '",'
        playlistIDStr += tempStr

    # Remove extra comma
    playlistLengthStr = '\'' + playlistLengthStr[:len(playlistLengthStr)-1] + ']\''
    playlistIDStr = '\'' + playlistIDStr[:len(playlistIDStr)-1] + ']\''

    # Set .env file
    with open(".env", "w") as envFile:

        # Update username
        envFile.write("USERNAME=" + username + '\n')

        # Update clientid
        envFile.write("CLIENTID=" + clientID + '\n')

        # Update clientsecret
        envFile.write("CLIENTSECRET=" + clientSecret + '\n')

        # Update amplaylistlengths
        envFile.write("AMPLAYLISTLENGTHS=" + playlistLengthStr + '\n')

        # Update playlists
        envFile.write("PLAYLISTS=" + playlistIDStr)

    print('[Update] Finished setting up your environment file.')
    print('[Update] Setting up Spotify Cache...')
    
    promptAns = str(input('[Warning] The following process will open and close a tab in your web browser to setup the cache.\n Type \'Y\' to proceed or \'N\' to cancel: '))

    if(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):

        print('[Update] Creating cache. This process may take several minutes...')

        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=clientID,
                                                client_secret=clientSecret,
                                                redirect_uri="http://localhost:1234/",
                                                scope="user-library-read"))

        spotifyScripts.get_track_info(sp, '4cOdK2wGLETKBW3PvgPWqT')

    else:
        print('[Update] Setup cancelled. Please follow the setup steps if you wish to install Spotify to MP3 in the future.')
        exit()

    print('[Update] Setup complete. Starting program...')
    # auth_url = 'https://accounts.spotify.com/api/token'

    # auth_headers = {
    #     "client_id": clientID,
    #     "response_type": "code",
    #     "redirect_uri": "http://localhost:1234/",
    #     "scope": "user-library-read"
    # }

    # webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))
    
    # code = str(input("Please input the auth code: "))

    # encoded_credentials = base64.b64encode(clientID.encode() + b':' + clientSecret.encode()).decode("utf-8")

    # token_headers = {
    #     "Authorization": "Basic " + encoded_credentials,
    #     "Content-Type": "application/x-www-form-urlencoded"
    # }

    # token_data = {
    #     "grant_type": "authorization_code",
    #     "code": code,
    #     "redirect_uri": "http://localhost:7777/callback"
    # }

    # data = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

    # token = data.json()["access_token"]

    # print(token)
    # print("here")
    # auth_response = requests.post(auth_url, data=data)

    # token = auth_response.json().get('access_token')

    # print(token)    

# RUN SETUP
initialSetup()