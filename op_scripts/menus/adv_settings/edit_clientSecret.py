"""
Module dedicated to editing Spotify client secret.
"""

import os
import dotenv

def edit_clientSecret():
    
    print('Current Spotify Client Secret: ' + str(os.environ.get('CLIENTSECRET')))
    inputStr = input('Please enter a new Spotify Client Secret to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['CLIENTSECRET'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "CLIENTSECRET", os.environ['CLIENTSECRET'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')