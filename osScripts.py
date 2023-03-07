import os
import time
import requests

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

def create_album_dir(newAlbums=list):
    """
    Creates directories for albums passed in.
    """

    musicDir = os.getcwd()
    musicDir = os.path.join(musicDir, "Music")

    for album in newAlbums:

        # If 'Music' directory exists, change directory into 'Music directory.
        try:

            os.chdir(musicDir)

        # If 'Music' directory doesn't exist, create 'Music' directory.
        except:
            
            os.mkdir(musicDir)

        finally:

            # If album doesn't exist, create album directory.
            try:

                os.chdir(musicDir)
                newAlbumDir = os.path.join(musicDir, album)
                os.mkdir(newAlbumDir)

            # If album already exists, ___.
            except:
                
                pass
            
    # Create text file containing time-stamped update
    preformattedTime = time.localtime()
    formattedTime = time.strftime("%m-%d-%Y %H:%M:%S", preformattedTime)
    
    with open('New Songs (' + formattedTime + ')', 'a') as playlist:
        
        pass


    updateFile = open('New Songs (' + formattedTime + ')', 'w')


def get_dir_file_count(baseDir=str):
    """
    Returns file count for a given directory.
    """
    
    pass

def download_img(albumName=str, url=str):
    """
    Downloads the image from the provided url with the name of 'albumName'.jpg
    """
    response = requests.get(url)
    with open('%s.jpg' % albumName, 'wb') as imgFile:
        imgFile.write(response.content)