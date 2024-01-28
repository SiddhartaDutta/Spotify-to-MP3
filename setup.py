import getpass
from time import sleep

def initialSetup():

    print("[INFO] The following will setup Spotify-to-MP3 for you.")
    sleep(0.5)
    print("[INFO] Please enter the information as requested. All mistakes can be fixed later in settings...\n")
    sleep(0.5)

    saveDir = str(input('[INPUT] Please input the full path of your host directory: '))

    clientID = str(input("[INPUT] Please input your generated Spotify Client ID: "))
    clientSecret = str(input("[INPUT] Please input your generated Spotify Client Secret: "))

    # Get iBroadcast information
    run = True
    while run:
        promptAns = str(input('[INPUT] Would you like to connect to iBroadcast? Type \'Y\' for "Yes" or \'N\' for "No": '))
        if(promptAns.lower() == 'n' or promptAns.lower() == 'no'):
            updateIBroad = 'False'
            run = False
        elif(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):
            updateIBroad = 'True'
            run = False
        else:
            print('[ERROR] Invalid Input.')

    if updateIBroad == 'True':
        iBroadUser = str(input("[INPUT] Please enter your iBroadcast username: "))
        iBroadPswd = str(getpass.getpass("[INPUT] Please enter your iBroadcast password: "))
    else:
        iBroadUser = ''
        iBroadPswd = ''

    # Get number of playlists to be added
    numOfPlaylists = None
    while numOfPlaylists == None:
        try:
            numOfPlaylists = int(input("[INPUT] Please input the number of Spotify playlists you wish to update: "))
        except:
            print("[ERROR] Invalid input. Please input a number.")

    # Get playlist IDs and download counts
    playlistIDs = []
    playlistLengths = []
    iBroadIDs = []
    while(len(playlistIDs)) < numOfPlaylists:

        # Get Spotify playlist ID
        playlistIDs.append(input('[INPUT] Please input a playlist ID for playlist #' + str(len(playlistIDs) + 1) + ': '))
        
        # Get download count
        run = True
        while run:
            try:
                playlistLengths.append(str(int(input('[INPUT] Please input the number of songs already downloaded for the above playlist: '))))
                run = False
            except:
                print("[ERROR] Invalid input. Please input a number.")

        # Update iBroadcast
        if updateIBroad == 'True':
            iBroadIDs.append(input('[INPUT] Please input the corresponding iBroadcast playlist ID for the above playlist: '))

    # Format playlist arrays for env file addition
    playlistLengthStr = playlistIDStr = iBroadIDStr = '['
    for Length, spID in zip(playlistLengths, playlistIDs):

        # Process length
        tempStr = str(Length)
        tempStr = '"' + tempStr + '",'
        playlistLengthStr += tempStr

        # Process Spotify ID
        tempStr = str(spID)
        tempStr = '"' + tempStr + '",'
        playlistIDStr += tempStr

    if updateIBroad == 'True':
        for ibID in iBroadIDs:
            # Process iBroadcast ID
            tempStr = str(ibID)
            tempStr = '"' + tempStr + '",'
            iBroadIDStr += tempStr

    if numOfPlaylists == 0:
        playlistLengthStr = playlistLengthStr + ']'
        playlistIDStr = playlistIDStr + ']'
    else:
        playlistLengthStr = playlistLengthStr[:len(playlistLengthStr)-1] + ']'
        playlistIDStr = playlistIDStr[:len(playlistIDStr)-1] + ']'

    if updateIBroad == 'True':
        if numOfPlaylists == 0:
            iBroadIDStr = iBroadIDStr + ']'
        else:
            iBroadIDStr = '\'' + iBroadIDStr[:len(iBroadIDStr)-1] + ']\''
    else:
        iBroadIDStr = iBroadIDStr + ']'

    # Set .env file
    with open(".env", "w") as envFile:

        # Host directory
        envFile.write("HOSTDIR=\'" + saveDir + '\'\n')

        # Debug Mode flag
        envFile.write("DEBUGMODE=\'" + 'False' + '\'\n')

        # iBroadcast flag
        envFile.write("UPDATEIBROADCAST=\'" + str(updateIBroad) + '\'\n')

        # Sleep timer
        envFile.write("MENUSLEEP=\'0.25\'\n")

        # Update clientid
        envFile.write("SPOTIFYCLIENTID=\'" + clientID + '\'\n')

        # Update clientsecret
        envFile.write("SPOTIFYCLIENTSECRET=\'" + clientSecret + '\'\n')

        # Update ibroadcast username
        envFile.write("IBROADCASTUSER=\'" + iBroadUser + '\'\n')

        # Update ibroadcast password
        envFile.write("IBROADCASTPSWD=\'" + iBroadPswd + '\'\n')

        # Update spotify playlists
        envFile.write("SPOTIFYPLAYLISTS=" + playlistIDStr + '\n')

        # Update ibroadcast playlists
        envFile.write("IBROADCASTPLAYLISTS=" + iBroadIDStr + '\n')

        # Update download counts
        envFile.write("DOWNLOADCOUNTS=" + playlistLengthStr + '\n')
        
    print('[UPDATE] User data saved.\n')
