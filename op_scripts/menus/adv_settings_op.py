"""
Module dedicated to settings menu methods.
"""

import os
import json
import dotenv

import op_scripts.gen as gen
import op_scripts.spotify as spotify

from op_scripts.menus.adv_settings import edit_username
from op_scripts.menus.adv_settings import edit_clientID
from op_scripts.menus.adv_settings import edit_clientSecret
from op_scripts.menus.adv_settings import edit_downloadCounts
from op_scripts.menus.adv_settings import edit_spotifyPlaylistIDs


operations = [(edit_username.edit_username, 'Edit Spotify Username'),
              (edit_clientID.edit_clientID, 'Edit Spotify Client ID'),
              (edit_clientSecret.edit_clientSecret, 'Edit Spotify Client Secret'),
              (edit_downloadCounts.edit_downloadCounts, 'Edit Downloaded Song Counts'),
              (edit_spotifyPlaylistIDs.edit_spotifyPlaylistIDs, 'Edit Spotify Playlist IDs'),
              (None, 'Back to Main Menu')
              ]

def run():

    run = True

    while run:

        printMenu()

        userInput = gen.input_verification(len(operations)) - 1

        if userInput == len(operations) - 1:
            #print('Quitting...\n')
            run = False
            break

        operations[userInput][0]()


def printMenu():

    print('---**--**--- ADVANCED SETTINGS ---**--**---\n')

    for tupleIndex in range(len(operations)):
        print(f'{tupleIndex + 1}. {operations[tupleIndex][1]}')

    print('\n-----***----- - - * *** * - - -----***-----\n')

def editEnvVars():
    """
    
    """
#44
    while True:
        print('---**--**--- ADVANCED SETTINGS ---**--**---\n')

        print("Please enter the number of the variable you wish to edit:")
        print("1. Spotify Username")
        print("2. Spotify Client ID")
        print("3. Spotify Client Secret")
        print("4. Playlist Currently Downloaded Counts")
        print("5. Spotify Playlist IDs")
        print("6. Back to Main Menu")

        print('\n-----***----- - - * *** * - - -----***-----\n')

        userInput = gen.input_verification(6)

        match userInput:
            case 1:     # Change Spotify username
                edit_username.editUsername()
            
            case 2:     # Change Client ID
                pass
            
            case 3:     # Change Client Secret
                print('Current Spotify Client Secret: ' + str(os.environ.get('CLIENTSECRET')))
                inputStr = input('Please enter a new Spotify Client Secret to use (leave blank to cancel): ')

                if len(inputStr):
                    os.environ['CLIENTSECRET'] = inputStr
                    dotenv.set_key(dotenv.find_dotenv(), "CLIENTSECRET", os.environ['CLIENTSECRET'])
                    print('Saved.\n')

                else:
                    print('Operation Aborted.\n')
            
            case 4:     # Change Download Counts
                print('Current Playlist IDs and Download Count: ')
                playlistIDs = json.loads(os.environ['PLAYLISTS'])
                AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

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
                        
                        AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])
                        
                        AMPlaylistLengths[userSelect - 1] = newLength
                        
                        # Convert list to strings
                        newStr = '['
                        for entry in range(len(AMPlaylistLengths)):
                                tempStr = str(AMPlaylistLengths[entry])
                                tempStr = '"' + tempStr + '",'
                                newStr += tempStr
                        newStr = newStr[:len(newStr)-1] + ']'
                        os.environ['AMPLAYLISTLENGTHS'] = str(newStr)
                        dotenv.set_key(dotenv.find_dotenv(), "AMPLAYLISTLENGTHS", os.environ['AMPLAYLISTLENGTHS'])

                        print('Saved.\n')

            case 5:     # Edit Spotify playlist IDs
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


            case 6:
                break

            case _:
                print('[ERROR] Unexpected verified input. Please publish an issue on GitHub. The program will quit now.')
                print('Quitting...')
                break
