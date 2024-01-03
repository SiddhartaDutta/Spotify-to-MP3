import json
from time import sleep

def initialSetup():

    print("[INFO] The following will setup Spotify-to-MP3 for you.")
    sleep(0.5)
    print("[INFO] Please enter the information as requested. All mistakes can be fixed later in settings...")
    sleep(0.5)

    data = {"DEBUGMODE":"False",
            "UPDATEIBROADCAST":'',
            "SPOTIFYCLIENTID":'',
            "SPOTIFYCLIENTSECRET":'',
            "IBROADCASTUSER":'',
            "IBROADCASTPSWD":'',
            "NATIVEPLAYLISTS":{},
            "IBROADCASTPLAYLISTS":{}
            }

    data["SPOTIFYCLIENTID"] = str(input("[INPUT] Please input your generated Spotify Client ID: "))
    data["SPOTIFYCLIENTSECRET"] = str(input("[INPUT] Please input your generated Spotify Client Secret: "))

    # Get iBroadcast information
    run = True
    while run:
        promptAns = str(input('[INPUT] Would you like to connect to iBroadcast? Type \'Y\' for "Yes" or \'N\' for "No": '))
        if(promptAns.lower() == 'n' or promptAns.lower() == 'no'):
            data["UPDATEIBROADCAST"] = 'False'
            run = False
        elif(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):
            data["UPDATEIBROADCAST"] = 'True'
            run = False
        else:
            print('[ERROR] Invalid Input.')

    iBroadUpdate = data["UPDATEIBROADCAST"] == 'True'

    # Get number of playlists to be added
    numOfPlaylists = None
    while numOfPlaylists == None:
        try:
            numOfPlaylists = int(input("[INPUT] Please input the number of Spotify playlists you wish to update: "))
        except:
            print("[ERROR] Invalid input. Please input a number.")
    
    if iBroadUpdate:
        data["IBROADCASTUSER"] = str(input("[INPUT] Please enter your iBroadcast username: "))
        data["IBROADCASTPSWD"] = str(input("[INPUT] Please enter your iBroadcast password: "))

    # Get playlist IDs and download counts
    while(len(data["NATIVEPLAYLISTS"])) < numOfPlaylists:

        # Get Spotify playlist ID
        spotifyID = str(input('[INPUT] Please input a playlist ID for playlist #' + str(len(data["NATIVEPLAYLISTS"]) + 1) + ': '))
        
        # Get download count
        run = True
        while run:
            try:
                downloadCount = str(int(input('[INPUT] Please input the number of songs already downloaded for the above playlist: ')))
                run = False
            except:
                print("[ERROR] Invalid input. Please input a number.")

        # Update native
        data["NATIVEPLAYLISTS"].update({spotifyID : downloadCount})

        # Update iBroadcast
        if iBroadUpdate:
            data["IBROADCASTPLAYLISTS"].update({spotifyID : str(input('[INPUT] Please enter the corresponding iBroadcast playlist ID for the above playlist: '))})
        else:
            data["IBROADCASTPLAYLISTS"].update({spotifyID : ''})

    # Set .data.json file
    with open(".data.json", "w") as datafile:
        obj = json.dumps(data, indent= 4)
        datafile.write(obj)
        
    print('[Update] Finished setting up your data file.')

    print('[Update] Setup complete. Starting program...')  

# RUN SETUP
initialSetup()