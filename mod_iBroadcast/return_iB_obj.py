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
