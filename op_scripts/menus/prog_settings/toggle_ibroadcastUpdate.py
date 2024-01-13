"""
Module dedicated to toggling iBroadcast automatic updates.
"""

import os
import dotenv

from op_scripts.gen import yn_input

def toggle_ibroadcastUpdate():

    if os.environ.get('UPDATEIBROADCAST') == 'True':
        print('iBroadcast Connection: ENABLED')
        toToggle = yn_input('Would you like to disable the iBroadcast connection?')
        if toToggle:
            newVal = 'False'
    else:
        print('iBroadcast Connection: DISABLED')
        toToggle = yn_input('Would you like to enable the iBroadcast connection?')
        if toToggle:
            newVal = 'True'
    
    os.environ['UPDATEIBROADCAST'] = newVal
    dotenv.set_key(dotenv.find_dotenv(), "UPDATEIBROADCAST", os.environ['UPDATEIBROADCAST'])
    print('Saved.\n')
   