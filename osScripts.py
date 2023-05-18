import os
import glob
import time
import shutil
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

    # Based on if there are new albums to be processed (new albums implies new songs)
    newSongs = False

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

                newSongs = True

            # Even if album directory exists, set newSong flag to True
            except:
                newSongs = True

            # Once in directory, download image if image does not exist
            finally:

                pass
            
    # Create text file if new songs exist, reset newSong flag
    if newSongs:
        with open('Playlist Update: ' + playlistName, 'a') as playlist:
            newSongs = False

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

    jpgList = glob.glob('*.jpg')
    imageExists = False

    # Check if image exists
    for image in jpgList:
        if image == (albumName + '.jpg'):
            imageExists = True

    # If image doesn't exist, download image
    if not imageExists:
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

def download_songs_by_spotify_id(self, playlistName=str, IDs=[], amLength=int, spotifyLength=int):
    """
    Downloads all songs by their Spotify ID.
    """

    for index in range(amLength, spotifyLength):
        # Create string to search for song with
        track = spotifyScripts.get_track_info(self, IDs[index])
        searchString = track['artists'][0]['name'] + ' ' + track['name'] + ' Official Audio'

        # Extract ID3 data
        albumName = str(track['album']['name'])
        releaseDate = str(track['album']['release_date'])
        genre = 'Hip-Hop/Rap'
        title = str(track['name'])
        tracknumber = str(track['track_number']) + '/' + str(track['album']['total_tracks'])
        
            # Extract all album artists
        albumArtist = ''
        numArtistsOnAlbum = len(track['album']['artists'])
        for n in range(numArtistsOnAlbum):
            if n:
                albumArtist += ', '
        
            albumArtist += track['album']['artists'][n]['name']

            # Extract all song artists
        songArtist = ''
        numArtistsOnSong = len(track['artists'])
        for n in range(numArtistsOnSong):
            if n:
                songArtist += ', '

            songArtist += track['artists'][n]['name']

        # Download song and edit ID3 tags
        with YoutubeDL(ydl_opts) as ydl:

            # Get URL for song
            videoURL = ydl.extract_info(f'ytsearch:{searchString}', download=False)['entries'][0]['webpage_url']
    
            # Change directory to add song to correct album folder
            currDir = os.getcwd()
            musicDir = os.getcwd()
            musicDir = os.path.join(musicDir, "Music/" + str(track['album']['name']))
            os.chdir(musicDir)

            # Download song
            ydl.download(videoURL)

            # Rename last downloaded file
            listOfFiles = glob.glob("*.mp3")
            latestFile = max(listOfFiles, key=os.path.getctime)
            os.rename(latestFile, title + '.mp3')

            # Adjust path to newest song
            musicDir = os.path.join(musicDir, title + '.mp3')

            # Change ID3 tags
            add_easyid3_tags(musicDir, albumName, albumArtist, songArtist, releaseDate, genre, title, tracknumber)

            # Update "update" file
            os.chdir('../')
            with open('Playlist Update: ' + playlistName, 'a') as playlist:
                print('[UPDATING PLAYLIST LIST]\n')
                playlist.write('*\t' + 'ALBUM: ' + albumName)
                playlist.write('\n \t' + 'TITLE: ' + title + '\n\n')

            # Reset directory
            os.chdir(currDir)

            # Download album cover
            download_img(albumName, spotifyScripts.get_album_cover_url(self, IDs[index]))

def move_images_to_album_dirs():
    """
    Move images from base directory into album directories.
    """

    basePath = os.path.join(os.getcwd(), "Music/")
    imagePaths = glob.glob('*.jpg')

    for image in imagePaths:

        # Extract album name from image and create target path
        tempStr = image[:(len(image)-4)]
        tempTargetPath = os.path.join(basePath, tempStr, image)

        # Move images from main directory into album directories
        shutil.move(image, tempTargetPath)   

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

    print('\n[NEW FILE]\n' + tempFile.pprint() + '\n')

def add_img_to_id3_for_album(targetDirectory=str):
    """
    Edits all ID3 tags for songs in a directory.
    """

    currDir = os.getcwd()
    os.chdir(targetDirectory)

    # Get path of all .mp3 files and .jpg album cover file
    mp3Files = glob.glob('*.mp3')
    albumCoverPath = glob.glob('*.jpg')[0]

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

    os.chdir(currDir)

def update_img_tags():
    """
    Steps through directories applying saved image to ID3 album cover tag.
    """

    currDir = os.getcwd()

    # Switch into Music directory
    os.chdir(os.path.join(os.getcwd(), 'Music'))

    # Cache subdirectories
    dirPaths = glob.glob(f'{os.getcwd()}/*/')

    # Update
    for directory in dirPaths:
        add_img_to_id3_for_album(directory)

    os.chdir(currDir)
