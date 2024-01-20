"""
Module dedicated to toggling debug mode.
"""

import os
import dotenv

from op_scripts.gen import yn_input

def toggle_debug():

    if os.environ.get('DEBUGMODE') == 'True':
        print('Debug Mode: ENABLED')
        toToggle = yn_input('Would you like to disable debug mode?')
        if toToggle:
            newVal = 'False'
    else:
        print('Debug Mode: DISABLED')
        toToggle = yn_input('Would you like to enable debug mode?')
        if toToggle:
            newVal = 'True'
    
    # Update only if update exists
    if toToggle:
        os.environ['DEBUGMODE'] = newVal
        dotenv.set_key(dotenv.find_dotenv(), "DEBUGMODE", os.environ['DEBUGMODE'])
    print('Saved.\n')
   