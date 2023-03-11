import os
import glob
import json
import time
import pprint
import requests
import spotifyScripts
from yt_dlp import YoutubeDL
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3  
from mutagen.id3 import ID3, APIC, error

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

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
    }],
    'postprocessor_args': [
            '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False
}

def download_songs_by_spotify_id(self, IDs=[]):
    """
    Downloads all songs by their Spotify ID.
    """

    for ID in IDs:
        track = spotifyScripts.get_track_info(self, ID)
        searchString = track['artists'][0]['name'] + ' ' + track['name'] + ' Official Audio'
        track

        with YoutubeDL(ydl_opts) as ydl:
            videoURL = ydl.extract_info(f'ytsearch:{searchString}', download=False)['entries'][0]['webpage_url']

            #pprint(json.dumps(ydl.sanitize_info(ydl.extract_info(f'ytsearch:{searchString}', download=False))))
            ydl.download(videoURL)

def add_img_to_id3_for_album(directory=str):
    """
    Edits all ID3 tags for songs in a directory.
    """

    # Get path of all .mp3 files and .jpg album cover file
    mp3Files = glob.glob('*.mp3')
    albumCoverPath = glob.glob('.jpg')[0]

    for song in mp3Files:

        tempFile = MP3(song, ID3=ID3)

        # Add tags in-case there are none
        try:
            tempFile.add_tags()
        except error:
            pass

        # Add image to ID3 and save
        tempFile.tags.add(APIC(mime = 'image/jpeg', type = 3, desc = u'Cover', data = open(albumCoverPath, 'rb').read()))
        tempFile.save()

