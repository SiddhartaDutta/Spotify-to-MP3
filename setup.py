from time import sleep
import spotipy.util as util

def initialSetup():

    print("[INFO] The following will setup Spotify-to-MP3 for you.")
    sleep(0.5)
    print("[INFO] Please enter the information as requested...")
    sleep(0.5)

    username = str(input("[INPUT] Please enter your Spotify username: "))
    clientID = str(input("[INPUT] Please input your generated Client ID: "))
    clientSecret = str(input("[INPUT] Please input your generated Client Secret: "))

    # Get number of playlists to be added
    numOfPlaylists = None
    while numOfPlaylists == None:
        try:
            numOfPlaylists = int(input("[INPUT] Please input the number of Spotify playlists you wish to update: "))
        except:
            print("[ERROR] Invalid input. Please input a number.")

    # Get playlist IDs
    playlistIDs = []
    while(len(playlistIDs)) < numOfPlaylists:
        playlistIDs.append(str(input('[INPUT] Please input a playlist ID for playlist #' + str(len(playlistIDs)+1) + ': ')))

    # Get playlist downloaded
    playlistLengths = []
    while len(playlistLengths) < numOfPlaylists:
        try:
            playlistLengths.append(int(input('[INPUT] Please enter the current number of downloaded songs for playlist with ID ' + playlistIDs[len(playlistLengths)] + ': ')))
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
    if numOfPlaylists > 0:
        playlistLengthStr = '\'' + playlistLengthStr[:len(playlistLengthStr)-1] + ']\''
        playlistIDStr = '\'' + playlistIDStr[:len(playlistIDStr)-1] + ']\''

    # Generate Token
    token = None
    print('[Update] Setting up Spotify Cache...')
    
    promptAns = str(input('[Warning] The following process will open tab in your web browser and request authorization to setup a cache.\n Type \'Y\' to proceed or \'N\' to cancel: '))

    if(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):

        print('[Update] Creating cache. This process may take several minutes...')

        token = util.prompt_for_user_token(username=username,scope="user-library-read",client_id=clientID,client_secret=clientSecret,redirect_uri="http://localhost:1234/")

    else:
        print('[Update] Setup cancelled. Please follow the setup steps if you wish to install Spotify to MP3 in the future.')
        exit()

    # Set .env file
    with open(".env", "w") as envFile:

        # Update username
        envFile.write("USERNAME=" + username + '\n')

        # Update clientid
        envFile.write("CLIENTID=" + clientID + '\n')

        # Update clientsecret
        envFile.write("CLIENTSECRET=" + clientSecret + '\n')

        # Update token
        envFile.write("TOKEN=" + token + '\n')

        # Update amplaylistlengths
        envFile.write("AMPLAYLISTLENGTHS=" + playlistLengthStr + '\n')

        # Update playlists
        envFile.write("PLAYLISTS=" + playlistIDStr)

    print('[Update] Finished setting up your environment file.')

    print('[Update] Setup complete. Starting program...')  

# RUN SETUP
initialSetup()