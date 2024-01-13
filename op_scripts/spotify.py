"""
Module dedicated to Spotify specific methods.
"""

import os
import glob
import time
import shutil
import dotenv
import requests
from tqdm import tqdm
from mutagen.mp3 import MP3
from yt_dlp import YoutubeDL
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3  
from mutagen.id3 import ID3, APIC, error

import op_scripts.gen as gen
import op_scripts.meta_data_frame as metaDF

def get_track_info(self, songID):
    """
    Returns track info for a given track's Spotify ID.
    """

    urn = 'spotify:track:' + songID
    try:
        return self.track(urn)
    except:
        try:
            time.sleep(5.0)
            return self.track(urn)
        except:
            print('\n[ERROR] INVALID SONG ID: ' + songID)
        pass

def get_playlist_ids(self, username, playlist_id):
    """
    Returns list of track Spotify IDs for a given playlist's Spotify ID.
    """

    r = self.user_playlist_tracks(username,playlist_id)
    t = r['items']
    ids = []
    while r['next']:
        r = self.next(r)
        t.extend(r['items'])
    for s in tqdm(t, desc= 'Caching Spotify Track IDs', disable= (os.environ.get('DEBUGMODE') == 'True')): ids.append(s["track"]["id"])
    return ids

def get_albums_from_ids(self, amLength, spotifyLength, idList):
    """
    Returns list of album names for given Spotify track IDs without repetition.
    """

    # Array to hold album names
    albumNames = []

    # Iterate through idList (list of music ids)
    for index in tqdm(range(amLength, spotifyLength), desc= 'Caching Album Names', disable= (os.environ.get('DEBUGMODE') == 'True')):
        trackID = idList[index]
        track = get_track_info(self, trackID)

        # Only add if doesn't already exist in list
        try:
            albumNames.index(track['album']['name'])
        except:
            albumNames.append(track['album']['name'])

    return albumNames

def get_playlist_length(self, playlistId):
    """
    Takes a Spotify playlist ID and returns the playlist's length.
    """

    playlist = self.playlist_items(playlist_id=playlistId, offset=0, fields='items.track.id,total', additional_types=['track'])
    return playlist['total']

def get_album_cover_url(self, songID=str):
    """
    Returns 300x300 album cover image url.
    """

    attempts = 0
    while attempts < 5:
        try:
            return get_track_info(self, songID)['album']['images'][1]['url']
        except:
            gen.prnt('[TIMEOUT ERROR] WAITING...')
            time.sleep(3)
            gen.prnt('[RETRYING...]')

    print('[]')

# new method for outputting new track names with artists (from end of main.py)

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

    for album in tqdm(newAlbums, desc= 'Creating Album Directories', disable= (os.environ.get('DEBUGMODE') == 'True')):

        album = gen.remove_slashes(album)

        # If 'Music' directory exists, change directory into 'Music directory.
        try:

            os.chdir(musicDir)

        # If 'Music' directory doesn't exist, create 'Music' directory.
        except:
            
            os.mkdir(musicDir)
            os.chmod(musicDir, 0o777)

        finally:

            # If album doesn't exist, create album directory.
            try:

                os.chdir(musicDir)
                newAlbumDir = os.path.join(musicDir, album)
                os.mkdir(newAlbumDir)
                os.chmod(newAlbumDir, 0o777)

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

def __match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def download_songs_by_spotify_id(self,  IDs=[], amLength=int, spotifyLength=int, sourceURL='', metaData= metaDF.metaDataFrame(), imgDownloaded= False):
    """
    Downloads all songs by their Spotify ID.
    :param list metaData: test
    """

    newFiles = []

    for index in tqdm(range(amLength, spotifyLength), desc= 'Downloading Songs', disable= (os.environ.get('DEBUGMODE') == 'True')):

        if sourceURL == '':
            track = get_track_info(self, IDs[index])

        # Extract ID3 data
        if metaData.albumName == '':

            metaData.albumName = str(track['album']['name'])
            metaData.releaseDate = str(track['album']['release_date'])
            metaData.genre = 'Hip-Hop/Rap'
            metaData.title = gen.remove_slashes(str(track['name']))
            metaData.trackNumber = str(track['track_number']) + '/' + str(track['album']['total_tracks'])

                # Extract all album artists
            metaData.albumArtist = ''
            numArtistsOnAlbum = len(track['album']['artists'])
            for n in range(numArtistsOnAlbum):
                if n:
                    metaData.albumArtist += ', '
            
                metaData.albumArtist += track['album']['artists'][n]['name']

                # Extract all song artists
            metaData.songArtist = ''
            numArtistsOnSong = len(track['artists'])
            for n in range(numArtistsOnSong):
                if n:
                    metaData.songArtist += ', '

                metaData.songArtist += track['artists'][n]['name']
        
        # Determine set of download options
        if os.environ.get("DEBUGMODE") == 'True':
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                }],
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'outtmpl': 'NEW_MP3_FILE',
                'quiet' : False
            }

        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192'
                }],
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'outtmpl': 'NEW_MP3_FILE',
                'quiet' : True
            }

        # Download song and edit ID3 tags
        with YoutubeDL(ydl_opts) as ydl:

            # Change directory to add song to correct album folder
            currDir = os.getcwd()
            musicDir = os.getcwd()
            musicDir = os.path.join(musicDir, "Music/" + gen.remove_slashes(metaData.albumName))
            os.chdir(musicDir)

            successfulDownload = False
            tries = 0
            while not successfulDownload and tries < 3:
                try:

                    # Download song
                    if sourceURL == '':

                        searchString = track['artists'][0]['name'] + ' ' + track['name'] + ' Official Audio'

                        # Get URL for song
                        videoURL = ydl.extract_info(f'ytsearch:{searchString}', download=False)['entries'][0]['webpage_url']                        
                        ydl.download(videoURL)

                    else:
                        ydl.download(sourceURL)

                    successfulDownload = True
                except:
                    tries += 1
                    print('[ERROR] WAITING...\n')
                    time.sleep(10)
                    print('[RETRYING...]\n')

            os.chmod('NEW_MP3_FILE.mp3', 0o777)

            gen.prnt('\n[NORMALIZING AUDIO]\n')
            sound = AudioSegment.from_file("NEW_MP3_FILE.mp3", "mp3")
            normalized_sound = __match_target_amplitude(sound, -14.0)
            normalized_sound.export("NEW_MP3_FILE.mp3", format= "mp3")

            os.rename('NEW_MP3_FILE.mp3', gen.remove_slashes(metaData.title) + '.mp3')

            # Adjust path to newest song
            musicDir = os.path.join(musicDir, gen.remove_slashes(metaData.title) + '.mp3')

            # Record new paths
            newFiles.append(str(musicDir))

            # Change ID3 tags
            add_easyid3_tags(musicDir, metaData.albumName, metaData.albumArtist, metaData.songArtist, metaData.releaseDate, metaData.genre, metaData.title, metaData.trackNumber)

            # Reset directory
            os.chdir(currDir)

            # Download album cover
            if not imgDownloaded:
                download_img(gen.remove_slashes(metaData.albumName), get_album_cover_url(self, IDs[index]))

            # Reset meta data struct
            metaData.albumName = ''

    # Return new file paths
    return newFiles

def move_images_to_album_dirs():
    """
    Move images from base directory into album directories.
    """

    basePath = os.path.join(os.getcwd(), "Music/")
    imagePaths = glob.glob('*.jpg')

    for image in tqdm(imagePaths, desc= 'Moving Images to Album Directories', disable= (os.environ.get('DEBUGMODE') == 'True')):

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
        gen.prnt('[UPDATE] Tag base already exists.')
        pass

    tempFile['album'] = albumName
    tempFile['albumartist'] = albumArtist
    tempFile['artist'] = songArtist
    tempFile['date'] = releaseDate
    tempFile['genre'] = genre
    tempFile['title'] = title
    tempFile['tracknumber'] = tracknumber

    tempFile.save()

    gen.prnt('\n[NEW FILE]\n' + tempFile.pprint() + '\n')

def add_img_to_id3_for_album(targetDirectory=str):
    """
    Edits image ID3 tag for songs in a directory.
    """
    #print(targetDirectory)
    currDir = os.getcwd()
    os.chdir(targetDirectory)

    # Get path of all .mp3 files and .jpg album cover file
    mp3Files = glob.glob('*.mp3')
    albumCoverPath = ''.join(glob.glob('*.jpg'))

    for song in mp3Files:

        tempFile = MP3(song, ID3=ID3)

        # Add tags in-case there are none
        try:
            tempFile.add_tags()
        except error:
            pass

        # Add image to ID3 and save
        #print(albumCoverPath)
        if not albumCoverPath == '':
            #print(albumCoverPath)
            tempFile.tags.add(APIC(mime = 'image/jpeg', type = 3, desc = u'Cover', data = open(albumCoverPath, 'rb').read()))
            tempFile.save()
        else:
            gen.prnt('[ERROR: .JPG NOT FOUND] ALBUM: ' + targetDirectory)

    # Delete image file
    try:
        os.remove(albumCoverPath)
    except:
        pass
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
    for directory in tqdm(dirPaths, desc= 'Applying Images to MP3 Files', disable= (os.environ.get('DEBUGMODE') == 'True')):
        add_img_to_id3_for_album(directory)

    os.chdir(currDir)

def write_playlist_data_to_env(playlistIDs, AMPlaylistLengths):

    # Format playlist arrays for env file addition
    playlistLengthStr = playlistIDStr = '['
    for Length, ID in zip(AMPlaylistLengths, playlistIDs):

        # Process length
        tempStr = str(Length)
        tempStr = '"' + tempStr + '",'
        playlistLengthStr += tempStr

        # Process ID
        tempStr = str(ID)
        tempStr = '"' + tempStr + '",'
        playlistIDStr += tempStr

    # Remove extra comma
    #if len(playlistIDs) > 0:
    if len(playlistIDs) == 0:
        playlistLengthStr = playlistLengthStr + ']'
        playlistIDStr = playlistIDStr + ']'
    else:
        playlistLengthStr = playlistLengthStr[:len(playlistLengthStr)-1] + ']'
        playlistIDStr = playlistIDStr[:len(playlistIDStr)-1] + ']'

    # Write to env file
    os.environ["SPOTIFYPLAYLISTS"] = playlistIDStr
    dotenv.set_key(dotenv.find_dotenv(), "SPOTIFYPLAYLISTS", os.environ["SPOTIFYPLAYLISTS"])

    os.environ["DOWNLOADCOUNTS"] = playlistLengthStr
    dotenv.set_key(dotenv.find_dotenv(), "DOWNLOADCOUNTS", os.environ["DOWNLOADCOUNTS"])
