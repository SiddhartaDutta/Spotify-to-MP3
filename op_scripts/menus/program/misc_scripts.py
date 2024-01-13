"""
Module dedicated to random/misc scripts relating to the program's primary operations.
"""

import os
import glob
import json
import dotenv

import op_scripts.spotify as spotify
import op_scripts.ibroadcast as ibroadcast

from op_scripts.gen import loading_screen, prnt

def upload_and_add_all(self):

    # Get Spotify playlist IDs & Apple Music playlist lengths
    playlistIDs = json.loads(os.environ['SPOTIFYPLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['DOWNLOADCOUNTS'])
    iBroadcastIDs = json.loads(os.environ['IBROADCASTPLAYLISTS'])

    if len(playlistIDs) == 0:
        print('[UPDATE] No playlists available. Please add playlists from the advanced menu.\n')
        return

    # Iterate through each Spotify playlist and compare length to downloaded counts
    for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotify.get_playlist_length(self, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

            newFiles = []
            currDir = os.getcwd()
            # Switch into Music directory
            musicDir = os.path.join(os.getcwd(), 'Music')
            os.chdir(musicDir)

            # Cache subdirectories
            dirPaths = glob.glob(f'{os.getcwd()}/*/')

            # For each music folder,
            for path in dirPaths:

                # Change to album folder
                os.chdir(path)

                temp = (glob.glob(f'{os.getcwd()}/*.mp3'))
                newFiles += temp

                os.chdir(musicDir)

            #print(newFiles)
            #return

            # Update iBroadcast if flagged
            if os.environ.get("UPDATEIBROADCAST") == 'True':
                prnt('[UPDATING iBROADCAST]\n')
                ibroadcast.upload_new(newFiles, iBroadcastIDs[playlist])

            os.chdir(currDir)

            # Update Apple Music playlist lengths automatically
            prnt('[UPDATING ENVIRONMENT VARIABLES]\n')
            AMPlaylistLengths[playlist] = currentSpotifyLength
                    # Convert list to strings
            newStr = '['
            for entry in range(len(AMPlaylistLengths)):
                    tempStr = str(AMPlaylistLengths[entry])
                    tempStr = '"' + tempStr + '",'
                    newStr += tempStr
            newStr = newStr[:len(newStr)-1] + ']'
            os.environ['DOWNLOADCOUNTS'] = str(newStr)
            dotenv.set_key(dotenv.find_dotenv(), "DOWNLOADCOUNTS", os.environ['DOWNLOADCOUNTS'])

            active = False
            print('[PLAYLIST UPDATE COMPLETE] PLAYLIST: %-*s NEW LENGTH: %s\n' % (25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
        else:
            print("[NO UPDATE AVAILABLE] %-*s PLAYLIST: %-*s CURRENT LENGTH: %s\n" % (4, '', 25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
