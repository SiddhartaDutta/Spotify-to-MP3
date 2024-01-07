"""
Module dedicated to settings menu methods.
"""

import os
import json
import dotenv

import op_scripts.gen as gen
import op_scripts.spotify as spotify

from op_scripts.menus.prog_settings import edit_username
from op_scripts.menus.prog_settings import edit_clientID
from op_scripts.menus.prog_settings import edit_clientSecret
from op_scripts.menus.prog_settings import edit_downloadCounts
from op_scripts.menus.prog_settings import edit_spotifyPlaylistIDs


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
