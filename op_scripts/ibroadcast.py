"""
Module dedicated to iBroadcast specific methods.
"""

import os
import ibroadcast

def return_iB_obj():
    """
    Returns iBroadcast object if credentials are accurate
    """
    user = os.environ.get("IBROADCASTUSER")
    pswd = os.environ.get("IBROADCASTPSWD")

    try:
        return ibroadcast.iBroadcast(user, pswd)
    except:
        print('[ERROR] No/incorrect iBroadcast credentials. Please check your username and password in Advanced Settings.')
        return None

def upload_ibroadcast():
    # isuploaded
    # upload
        # record returned ids
    # addtracks
    # notes:
    # - will be added near line 70 auto_update.py
    # - will probably need all track names prior to upload to know what to upload
        # - make a list of paths with spotify track ids?
    pass