"""
Module dedicated to editing Spotify Client ID.
"""

import os
import dotenv

def edit_clientID():
    
    print('Current Spotify Client ID: ' + str(os.environ.get('SPOTIFYCLIENTID')))
    inputStr = input('Please input a new Spotify Client ID to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['SPOTIFYCLIENTID'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "SPOTIFYCLIENTID", os.environ['SPOTIFYCLIENTID'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')