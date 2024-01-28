"""
Module dedicated to editing the user's iBroadcast username.
"""

import os
import dotenv

def edit_ibroadcastUser():
    
    print('Current iBroadcast Username: ' + str(os.environ.get('IBROADCASTUSER')))
    inputStr = input('Please enter a new iBroadcast username to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['IBROADCASTUSER'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "IBROADCASTUSER", os.environ['IBROADCASTUSER'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')