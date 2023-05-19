import os
import json
import dotenv

import osScripts
import spotifyScripts

def run(self):
    printMenu()

    userInput = inputVerification()

    match userInput:
        case 1:
            autoUpdate(self)
        case 2:
            sourceAndSpotify(self)
        case _:
            print('here')

def inputVerification():
    userIn = None
     
    while userIn is None:
        try:
            userIn = int(input('Please Input Selection: '))
            if userIn > 2:
                userIn = None
                raise ValueError()
        except ValueError:
             print('Invalid Input.')

    return userIn
    

def printMenu():
    print('To automatically run checks on provided Spotify playlist IDs %-*s' % (10, 'Type 1'))
    #print('To assign single source to single existing song %-*s' % (20, 'Type 2'))

    print()
    

def autoUpdate(self):
    # *****         MAIN SCRIPT         *****

    # Get Spotify playlist IDs & Apple Music playlist lengths
    playlistIDs = json.loads(os.environ['PLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

    # Iterate through each Spotify playlist and compare length to Apple Music lengths
    for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotifyScripts.get_playlist_length(self, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

            # Get song IDs for non-equal Spotify playlist
            print('[CACHING SONG IDS]\n')
            songIDs = spotifyScripts.get_playlist_ids(self, os.environ.get("USERNAME"), playlistIDs[playlist])

            # Get albums of missing songs
            print('[CACHING ALBUM NAMES OF MISSING SONGS]\n')
            newAlbums = spotifyScripts.get_albums_from_ids(self, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)

            # Make directories
            print('[CREATING ALBUM DIRECTORIES]\n')
            osScripts.create_album_dirs((self.playlist(playlistIDs[playlist]))['name'], newAlbums)

            # Download songs & images
            print('[DOWNLOADING SONGS AND ALBUM COVERS]\n')
            osScripts.download_songs_by_spotify_id(self, (self.playlist(playlistIDs[playlist]))['name'], songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

            # Move images
            print('[MOVING .JPG FILES]\n')
            osScripts.move_images_to_album_dirs()

            # Update all image tags
            print('[UPDATING ID3 IMAGE TAGS]\n')
            osScripts.update_img_tags()

            # Update Apple Music playlist lengths automatically
            print('[UPDATING ENVIRONMENT VARIABLES]\n')
            AMPlaylistLengths[playlist] = currentSpotifyLength
                    # Convert list to strings
            newStr = '['
            for entry in range(len(AMPlaylistLengths)):
                    tempStr = str(AMPlaylistLengths[entry])
                    tempStr = '"' + tempStr + '",'
                    newStr += tempStr
            newStr = newStr[:len(newStr)-1] + ']'
            os.environ['AMPLAYLISTLENGTHS'] = str(newStr)
            dotenv.set_key(dotenv.find_dotenv(), "AMPLAYLISTLENGTHS", os.environ['AMPLAYLISTLENGTHS'])

            print('[PLAYLIST UPDATE COMPLETE] PLAYLIST: %-*s NEW LENGTH: %s\n' % (25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
        else:
            print("[NO UPDATE AVAILABLE] %-*s PLAYLIST: %-*s CURRENT LENGTH: %s\n" % (4, '', 25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))

def sourceAndSpotify(self):
    pass
