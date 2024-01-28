"""
Module dedicated to editing the user's iBroadcast password.
"""

import os
import dotenv
import getpass

from op_scripts.gen import yn_input

def edit_ibroadcastPass():
    
    print('Would you like to view current password? (WARNING: Your password WILL BE DISPLAYED and not cleared until after a new one is saved or the operation is cancelled.)')
    display = yn_input(prompt= '')
    
    # Display only if user approves
    if display:
        print('Current iBroadcast Password: ' + str(os.environ.get('IBROADCASTPSWD')))
    else:
        print('Current password will not be displayed.')

    # Continue operation
    inputStr = getpass.getpass('\nPlease enter a new iBroadcast password to use (leave blank to cancel): ')

    if len(inputStr):
        os.environ['IBROADCASTPSWD'] = inputStr
        dotenv.set_key(dotenv.find_dotenv(), "IBROADCASTPSWD", os.environ['IBROADCASTPSWD'])
        print('Saved.\n')

    else:
        print('Operation Aborted.\n')