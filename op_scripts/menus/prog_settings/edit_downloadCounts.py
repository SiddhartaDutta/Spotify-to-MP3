"""
Module dedicated to editing downloaded song counts.
"""

import os
import json
import dotenv

import op_scripts.gen as gen

def edit_downloadCounts():

    print('Current Playlist IDs and Download Count: ')
    playlistIDs = json.loads(os.environ['SPOTIFYPLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['DOWNLOADCOUNTS'])

    # Print all playlists and counts
    for playlist in range(len(playlistIDs)):
        print('\t' + str(playlist + 1) + '. ' + str(playlistIDs[playlist]) + ': ' + str(AMPlaylistLengths[playlist]))

    # Get playlist to change
    print()
    userSelect = gen.input_verification(len(playlistIDs), blankInput= True, prompt= 'Please enter a playlist number')

    if not userSelect and userSelect != 0:

        print('Operation Aborted.\n')

    else:

        newLength = str(input('Please enter new playlist length (leave blank to cancel): '))

        if not newLength and newLength != 0:

            print('Operation Aborted.\n')

        else:
            
            AMPlaylistLengths = json.loads(os.environ['DOWNLOADCOUNTS'])
            
            AMPlaylistLengths[userSelect - 1] = newLength
            
            # Convert list to strings
            newStr = '['
            for entry in range(len(AMPlaylistLengths)):
                    tempStr = str(AMPlaylistLengths[entry])
                    tempStr = '"' + tempStr + '",'
                    newStr += tempStr
            newStr = newStr[:len(newStr)-1] + ']'
            os.environ['DOWNLOADCOUNTS'] = str(newStr)
            dotenv.set_key(dotenv.find_dotenv(), "DOWNLOADCOUNTS", os.environ['DOWNLOADCOUNTS'])

            print('Saved.\n')