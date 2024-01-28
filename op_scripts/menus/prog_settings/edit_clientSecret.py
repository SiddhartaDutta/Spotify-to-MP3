"""
Module dedicated to editing Spotify client secret.
"""

import os
import dotenv

def edit_clientSecret():
    
    print('Current Spotify Client Secret: ' + str(os.environ.get('SPOTIFYCLIENTSECRET')))
    inputStr = input('Please enter a new Spotify Client Secret to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['SPOTIFYCLIENTSECRET'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "SPOTIFYCLIENTSECRET", os.environ['SPOTIFYCLIENTSECRET'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')