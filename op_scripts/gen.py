"""
Module dedicated to general operation methods.
"""

import sys
import time
import itertools

def get_dir_file_count(baseDir=str):
    """
    Returns file count for a given directory.
    """
    
    pass

def remove_slashes(string=str):
    """
    Replaces all slashes in a string.
    """
    return string.replace('/', '[ADD SLASH HERE]')

def modify_slashes(string=str):
    """
    """
    return string.replace('/', "[$KEY$]")

# create key to replace for slashes - replace in song name before creating file and etc.
# or- figure out how to replace name during download itself- like how u can thru terminal

def input_verification(maxCount = 0, ignoreMax = False, blankInput = False, stringInput = False, prompt = 'Please input selection'):
    """
    Modular input collection method.
    :param int maxCount: 
    :return: something
    """
    
    userIn = None
     
    while userIn is None:
        try:
            if not stringInput:
                if not blankInput:
                    userIn = int(input(prompt + ': '))
                else:
                    userIn = int(input(prompt + ' (leave blank to cancel): '))

                if userIn > maxCount and not ignoreMax:
                    #userIn = None
                    raise ValueError()
            else:
                if not blankInput:
                    userIn = input(prompt + ': ')
                else:
                    userIn = input(prompt + ' (leave blank to cancel): ')

            
        except ValueError:
            
             if blankInput and not userIn and userIn != 0:
                return userIn
             
             userIn = None
             print('Invalid Input.')

    print()
    return userIn

def loading_screen(active):
    for char in itertools.cycle(['', '.', '..', '...']):
        if not active():
            break
        sys.stdout.write('\rCreating File(s) ' + char)
        sys.stdout.flush()
        time.sleep(0.25)
    sys.stdout.write('\r\n')

def prnt(active, string):
    if active: print(string)