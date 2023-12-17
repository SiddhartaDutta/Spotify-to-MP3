"""
Module dedicated to editing stored Spotify playlist IDs.
"""

import os
import json

import op_scripts.gen as gen
import op_scripts.spotify as spotify

def edit_spotifyPlaylistIDs():

    print('Current Playlist IDs and Download Count: ')
    playlistIDs = json.loads(os.environ['PLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

    # Print all playlists and counts
    for playlist in range(len(playlistIDs)):
        print('\t' + str(playlist + 1) + '. ' + str(playlistIDs[playlist]) + ': ' + str(AMPlaylistLengths[playlist]))

    # Print 2 additional options
    print('\t' + str(len(playlistIDs) + 1) + '. Add playlist')
    print('\t' + str(len(playlistIDs) + 2) + '. Remove playlist')   

    print()
    userSelect = gen.input_verification(len(playlistIDs) + 2, blankInput= True)

    if not userSelect and userSelect != 0:

        print('Operation Aborted.\n')

    else:

        if userSelect == len(playlistIDs) + 1:        # Add Playlist
            newID = str(input('Please enter new playlist ID (leave blank to cancel): '))

            if not newID and newID != 0:
                print('Operation Aborted.\n')

            else:
                print()
                newCount = str(input('Please enter new playlist length (leave blank to cancel): '))

                if not newCount and newCount != 0:
                    print('Operation Aborted.\n')
                
                else:
                    if(len(newCount)):
                        playlistIDs = json.loads(os.environ['PLAYLISTS'])
                        AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

                        playlistIDs.append(newID)
                        AMPlaylistLengths.append(newCount)

                        spotify.write_playlist_data_to_env(playlistIDs, AMPlaylistLengths)
                        
                        print('Saved.\n')



        elif userSelect == len(playlistIDs) + 2:      # Remove playlist

            removeNum = gen.input_verification(maxCount= len(playlistIDs), blankInput= True, prompt= 'Please enter a playlist number to delete')

            if not removeNum and removeNum != 0:
                print('Operation Aborted.\n')
            
            else:

                # Reverify with warning
                numConfirm = gen.input_verification(maxCount= len(playlistIDs), blankInput= True, prompt= 'Please re-enter the playlist to delete (This action CANNOT be undone!)')

                if (not numConfirm and numConfirm != 0) or (removeNum != numConfirm):
                    print('Operation Aborted.\n')
                
                else:

                    playlistIDs = json.loads(os.environ['PLAYLISTS'])
                    AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

                    delID = playlistIDs.pop(numConfirm - 1)
                    delLength = AMPlaylistLengths.pop(numConfirm - 1)

                    spotify.write_playlist_data_to_env(playlistIDs= playlistIDs, AMPlaylistLengths= AMPlaylistLengths)
                    print('Saved.\n')
                    print('Successfully deleted playlist \'' + delID + '\' with length ' + delLength +'.\n')

        else:                           # Update playlist ID
            pass
