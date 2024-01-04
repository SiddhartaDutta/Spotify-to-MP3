"""
Module dedicated to iBroadcast specific methods.
"""

import os
import ibroadcast

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

def upload_to_ibroadcast(newFilePaths : list, iBroadcastPlaylistID):
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
    