import os
import time

def update_dir():
    """
    Creates a directory to hold all new songs for a given update. Directory name contains timestamp.
    """
    preformattedTime = time.localtime()
    formattedTime = time.strftime("%m-%d-%Y %H:%M:%S", preformattedTime)
    print(formattedTime)

    cwd = os.getcwd()
    pathExtension = "Music Update (" + formattedTime + ")"

    newPath = os.path.join(cwd, pathExtension)

    #os.mkdir(newPath)

def create_album_dir():

    musicDir = os.getcwd()
    musicDir = os.path.join(musicDir, "Music")

    try:

        os.chdir(musicDir)
        print('inside')

    except:
        
        os.mkdir(musicDir)
        print("new directory created")

    pass

def get_dir_file_count(baseDir):
    """
    Returns file count for a given directory.
    """
    
    pass

#update_dir()
create_album_dir()