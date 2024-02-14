import time
import errno
from tqdm import tqdm

from mod_iBroadcast.return_iB_obj import __return_iB_obj
from op_scripts.gen import prnt

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
    iBroadcastTrackIDs = [1]
    
    # For each new file, attempt to
    for file in tqdm(newFilePaths, desc= 'Uploading to iBroadcast', disable= (os.environ.get('DEBUGMODE') == 'True')):
        
        # Upload if not uploaded
        if True:
            
            # Prevent too many request timeout
            time.sleep(1.5)
            
            # Upload file
            attempts = 0
            while attempts < 5:
                try:
            
                    # Upload file
                    prnt('[UPDATE] Uploading: ' + file)
                    iBroadcastTrackIDs[0] = tempIBOBJ.upload(file, force= False)

                    # Add track to playlist
                    prnt('[UPDATE] Adding to playlist...')
                    tempIBOBJ.addtracks(iBroadcastPlaylistID, iBroadcastTrackIDs)

                    prnt('[UPDATE] SUCCESSFUL\n')
                    attempts = 10
                    break

                except MemoryError:

                    print('[ERROR] CRITICAL Memory Error. Program will be force shutting down...')
                    quit()

                except TimeoutError:
                    
                    tempList = []
                    tempList.append(file)
                    print('[ERROR] Connection Timed Out. Retrying...')

                    upload_new(tempList, iBroadcastPlaylistID= iBroadcastPlaylistID)

                except OSError as error:

                    _CONNECTION_ERRORS = frozenset({
                        errno.ECONNRESET,  # ConnectionResetError
                        errno.EPIPE, errno.ESHUTDOWN,  # BrokenPipeError
                        errno.ECONNABORTED,  # ConnectionAbortedError
                        errno.ECONNREFUSED,  # ConnectionRefusedError
                    })

                    if error.errno not in _CONNECTION_ERRORS:
                        raise
                    print('got ConnectionError - %e' % error)

                except:

                    print('[ERROR] Possible timeout. Waiting...')
                    time.sleep(10.0)
                    attempts += 1
                    print('[UPDATE] Retrying...')

            # Save file if not uploaded
            if attempts != 10:
                prnt('[ERROR] File could not be uploaded. Refer to \'SKIPPED.txt\' for file.')
                with open('SKIPPED.txt', 'a') as skipFile:
                    skipFile.write(str(file) + '\n')