"""
Module dedicated to settings menu methods.
"""

import os
from time import sleep

import op_scripts.gen as gen
from op_scripts.menus.prog_settings import edit_username
from op_scripts.menus.prog_settings import edit_clientID, edit_clientSecret
from op_scripts.menus.prog_settings import edit_downloadCounts
from op_scripts.menus.prog_settings import edit_spotifyPlaylistIDs
from op_scripts.menus.prog_settings import toggle_debug
from op_scripts.menus.prog_settings import toggle_ibroadcastUpdate
from op_scripts.menus.prog_settings import edit_ibroadcastUser, edit_ibroadcastPass


operations = [(edit_downloadCounts.edit_downloadCounts, 'Edit Downloaded Song Counts'),
              (edit_username.edit_username, 'Edit Spotify Username'),
              (edit_spotifyPlaylistIDs.edit_spotifyPlaylistIDs, 'Edit Spotify Playlist IDs (Modify, Add, Delete)'),
              (edit_clientID.edit_clientID, 'Edit Spotify Client ID'),
              (edit_clientSecret.edit_clientSecret, 'Edit Spotify Client Secret'),
              (toggle_debug.toggle_debug, 'Toggle Debug Mode'),
              (toggle_ibroadcastUpdate.toggle_ibroadcastUpdate, 'Toggle iBroadcast Connection'),
              (edit_ibroadcastUser.edit_ibroadcastUser, 'Edit iBroadcast Username'),
              (edit_ibroadcastPass.edit_ibroadcastPass, 'Edit iBroadcast Password'),
              (None, 'Back to Main Menu')
              ]

def run():

    run = True

    while run:

        sleep(float(os.environ.get('MENUSLEEP')))
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
