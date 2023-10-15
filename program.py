"""
Module dedicated to calling methods for menu operation.
"""

import op_scripts.gen as gen
import op_scripts.menus.settings as settings
import op_scripts.menus.auto_update as auto_update
import op_scripts.menus.create_song as create_song
import op_scripts.menus.spotify_base as spotify_base

def run(self):

    run = True

    while run:

        printMenu()

        userInput = gen.input_verification(5)

        match userInput:
            case 1:
                auto_update.autoUpdate(self)
            case 2:
                spotify_base.spotifyBase(self)
            case 3:
                createSong()
            case 4:
                settings.editEnvVars()
            case 5:
                print('Quitting...\n')
                run = False
            case _:
                print('[ERROR] Unexpected verified input. Please publish an issue on GitHub. The program will quit now.')
                print('Quitting...')
                run = False

def printMenu():

    print('-----***----- SPOTIFY TO MP3 -----***------\n')

    # Main menu operations
    print('1. Automatically Run Checks on Provided Spotify Playlist IDs')
    print('2. Assign a Source to Spotify Song')
    print('3. Create a Fully Custom Song')

    # Utility
    print('4. Edit Environment Variables')
    print('5. Exit the Program')

    print('\n-----***----- - - * ** * - - -----***------\n')
