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

def create_album_dirs(playlistName=str, newAlbums=list):
    """
    Creates directories for albums passed in.
    """

    currDir = os.getcwd()

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
    
    with open(playlistName + ' (' + formattedTime + ')', 'a') as playlist:
        
        pass


    #updateFile = open('New Songs (' + formattedTime + ')', 'w')

    # Change back to original directory
    os.chdir(currDir)


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

def download_songs_by_spotify_id(self, IDs=[], amLength=int, spotifyLength=int):
    """
    Downloads all songs by their Spotify ID.
    """

    for index in range(amLength, spotifyLength):
        track = spotifyScripts.get_track_info(self, IDs[index])
        searchString = track['artists'][0]['name'] + ' ' + track['name'] + ' Official Audio'

        # Extract ID3 data
        albumName = str(track['album']['name'])
        releaseDate = '2014'
        genre = 'Hip-hop'
        title = str(track['name'])
        tracknumber = str(track['track_number']) + '/' + str(track['album']['total_tracks'])
        
            # Extract all album artists
        albumArtist = ''
        numArtistsOnAlbum = len(track['album']['artists'])
        for index in range(numArtistsOnAlbum):
            if index:
                albumArtist += ', '
        
            albumArtist += track['album']['artists'][index]['name']

            # Extract all song artists
        songArtist = ''
        numArtistsOnSong = len(track['artists'])
        for index in range(numArtistsOnSong):
            if index:
                songArtist += ', '

            songArtist += track['artists'][index]['name']

        #pprint(track)

        with YoutubeDL(ydl_opts) as ydl:
            videoURL = ydl.extract_info(f'ytsearch:{searchString}', download=False)['entries'][0]['webpage_url']
    
            #pprint(json.dumps(ydl.sanitize_info(ydl.extract_info(f'ytsearch:{searchString}', download=False))))
            # Change directory to add song to correct album folder
            currDir = os.getcwd()
            musicDir = os.getcwd()
            musicDir = os.path.join(musicDir, "Music/" + str(track['album']['name']))
            os.chdir(musicDir)

            # Download song
            ydl.download(videoURL)

            # Rename
            listOfFiles = glob.glob("*.mp3")
            latestFile = max(listOfFiles, key=os.path.getctime)
            print(latestFile)
            print(musicDir)
            os.rename(latestFile, title + '.mp3')

            # Adjust path to newest song
            musicDir = os.path.join(musicDir, title + '.mp3')

            # Change ID3 tags
            add_easyid3_tags(musicDir, albumName, albumArtist, songArtist, releaseDate, genre, title, tracknumber)

            os.chdir(currDir)

def add_easyid3_tags(PATH, albumName, albumArtist, songArtist, releaseDate, genre, title, tracknumber):
    """
    Added EasyID3 tags to each song from provided data.
    """

    tempFile = MP3(PATH, ID3=EasyID3)

    try:
        tempFile.add_tags()
    except error:
        pass

    tempFile['album'] = albumName
    tempFile['albumartist'] = albumArtist
    tempFile['artist'] = songArtist
    tempFile['date'] = releaseDate
    tempFile['genre'] = genre
    tempFile['title'] = title
    tempFile['tracknumber'] = tracknumber

    tempFile.save()

    print(tempFile.pprint())

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

