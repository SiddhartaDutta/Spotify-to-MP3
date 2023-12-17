"""
Module dedicated to calling methods for menu operation.
"""

import op_scripts.gen as gen
import op_scripts.menus.adv_settings_op as adv_settings_op
import op_scripts.menus.program.auto_update as auto_update
import op_scripts.menus.program.create_song as create_song
import op_scripts.menus.program.create_album as create_album
import op_scripts.menus.program.spotify_base as spotify_base



operations = [(auto_update.autoUpdate, True, 'Automatically Run Checks on Provided Spotify Playlist IDs'),
              (spotify_base.spotifyBase, True, 'Assign a SoundCloud Source to Spotify Song'),
              (create_song.createSong, False, 'Create a Fully Custom Song'),
              (create_album.createAlbum, False, 'Create a Fully Custom Album'),
              (adv_settings_op.run, False, 'Advanced Settings'),
              (None, False, 'Exit the Program')
             ]

def run(self):

    run = True

    while run:
        
        printMenu()

        userInput = gen.input_verification(len(operations)) - 1

        if userInput == len(operations) - 1:
            print('Quitting...\n')
            run = False
            break

        choice = operations[userInput]

        if choice[1]:
            choice[0](self)
        else:
            choice[0]()

def printMenu():

    print('------***----- SPOTIFY TO MP3 -----***------\n')

    for tupleIndex in range(len(operations)):
        print(f'{tupleIndex + 1}. {operations[tupleIndex][2]}')

    print('\n-----***----- - - * **** * - - -----***-----\n')
