"""
Module dedicated to settings menu methods.
"""

from time import sleep

import op_scripts.gen as gen
from op_scripts.menus.prog_settings import edit_username
from op_scripts.menus.prog_settings import edit_clientID
from op_scripts.menus.prog_settings import edit_clientSecret
from op_scripts.menus.prog_settings import edit_downloadCounts
from op_scripts.menus.prog_settings import edit_spotifyPlaylistIDs
from op_scripts.menus.prog_settings import toggle_debug
from op_scripts.menus.prog_settings import toggle_ibroadcastUpdate


operations = [(edit_username.edit_username, 'Edit Spotify Username'),
              (toggle_ibroadcastUpdate.toggle_ibroadcastUpdate, 'Toggle iBroadcast Connection'),
              (edit_downloadCounts.edit_downloadCounts, 'Edit Downloaded Song Counts'),
              (edit_spotifyPlaylistIDs.edit_spotifyPlaylistIDs, 'Edit Spotify Playlist IDs'),
              (edit_clientID.edit_clientID, 'Edit Spotify Client ID'),
              (edit_clientSecret.edit_clientSecret, 'Edit Spotify Client Secret'),
              (toggle_debug.toggle_debug, 'Toggle Debug Mode'),
              (None, 'Back to Main Menu')
              ]

def run():

    run = True

    while run:

        sleep(0.75)
        gen.clear_screen()

        printMenu()

        userInput = gen.input_verification(len(operations)) - 1

        if userInput == len(operations) - 1:
            #print('Quitting...\n')
            run = False
            break

        operations[userInput][0]()


def printMenu():

    print('-----**--**----- SETTINGS -----**--**-----\n')

    for tupleIndex in range(len(operations)):
        print(f'{tupleIndex + 1}. {operations[tupleIndex][1]}')

    print('\n-----***----- - - * ** * - - -----***-----\n')