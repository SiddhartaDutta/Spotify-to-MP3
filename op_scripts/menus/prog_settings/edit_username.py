"""
Module dedicated to editing Spotify username.
"""

import os
import dotenv

def edit_username():

    print('Current Spotify username: ' + str(os.environ.get('USERNAME')))
    print(str(os.environ.get('USERNAME')))
    inputStr = input('Please enter a new Spotify username to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['USERNAME'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "USERNAME", os.environ['USERNAME'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')