"""
Module dedicated to iBroadcast specific methods.
"""

import os
import glob
import threading
import ibroadcast

from op_scripts.gen import prnt, loading_screen

def __return_iB_obj():
    """
    Returns iBroadcast object if credentials are accurate
    """

    user = os.environ.get("IBROADCASTUSER")
    pswd = os.environ.get("IBROADCASTPSWD")

    try:
        return ibroadcast.iBroadcast(user, pswd)
    except:
        print('[ERROR] No/incorrect iBroadcast credentials. Please check your username and password in Advanced Settings.')
        print('[UPDATE] Aborting...')
        return None

def upload_new(newFilePaths : list, iBroadcastPlaylistID):
    """
    Uploads new tracks to iBroadcast
    """

    # Abort if no new files for playlist
    if newFilePaths == None:
        return

    # Abort if user credentials are wrong
    tempIBOBJ = __return_iB_obj()
    if tempIBOBJ == None:
        return
    
    # iBroadcast returned track ids for playlist assignment 
    iBroadcastTrackIDs = []
    
    # For each new file, attempt to
    for file in newFilePaths:
        
        # Upload if not uploaded
        if not tempIBOBJ.isuploaded(file):

            # Upload file
            iBroadcastTrackIDs.append(tempIBOBJ.upload(file))

    # Add tracks to playlist
    tempIBOBJ.addtracks(iBroadcastPlaylistID, iBroadcastTrackIDs)
    
def upload_all():
    """
    Attempts to upload all files in 'Music' directory to iBroadcast
    """

    # Abort if user credentials are wrong
    tempIBOBJ = __return_iB_obj()
    if tempIBOBJ == None:
        return
    
    # Start loading animation
    print('[UPDATE] This process can take several minutes. Do *NOT* force quit the program!\n')
    active = True
    loadThread = threading.Thread(target= loading_screen, args= (lambda : active, ))
    loadThread.start()

    # Store default path
    currPath = os.getcwd()

    # Switch into Music directory
    musicDir = os.path.join(os.getcwd(), 'Music')
    os.chdir(musicDir)

    # Cache subdirectories
    dirPaths = glob.glob(f'{os.getcwd()}/*/')

    # For each music folder,
    for path in dirPaths:

        # Change to album folder
        os.chdir(path)

        songPaths = glob.glob(f'{os.getcwd()}/*.mp3')

        # For each song,
        for song in songPaths:

        # Upload if not uploaded
            if not tempIBOBJ.isuploaded(song):

                # Upload file
                prnt('[UPDATE] UPLOADING: ' + song)
                tempIBOBJ.upload(song)
                prnt('[UPDATE] UPLOADED: ' + song + '\n')

        # Back out of album folder
        os.chdir(musicDir)

    os.chdir(currPath)
    active = False

    print('\n\n[UPDATE] All files from \'Music\' not uploaded to iBroadcast now uploaded.\n')

def update_playlists():
    pass