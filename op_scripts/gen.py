"""
Module dedicated to general operation methods.
"""

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

def input_verification(maxCount, ignoreMax = False, blankInput = False, prompt = 'Please input selection'):
    """
    Modular input collection method.
    :param int maxCount: 
    :return: something
    """
    
    userIn = None
     
    while userIn is None:
        try:
            if not blankInput:
                userIn = int(input(prompt + ': '))
            else:
                userIn = int(input(prompt + ' (leave blank to cancel): '))

            if userIn > maxCount and not ignoreMax:
                #userIn = None
                raise ValueError()
            
        except ValueError:
            
             if blankInput and not userIn and userIn != 0:
                return userIn
             
             userIn = None
             print('Invalid Input.')

    print()
    return userIn