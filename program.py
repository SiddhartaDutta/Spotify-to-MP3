import os
import json
import dotenv

import op_scripts.gen as gen
import op_scripts.spotify as spotify
import op_scripts.settings as settings

def run(self):

    run = True

    while run:

        printMenu()

        userInput = gen.input_verification(5)

        match userInput:
            case 1:
                autoUpdate(self)
            case 2:
                sourceAndSpotify(self)
            case 3:
                createSong()
            case 4:
                settings.editEnvVars()
            case 5:
                print('Quitting...\n')
                run = False
            case _:
                print('[ERROR] Unexpected verified input. Please publish an issue on GitHub. The program will quit now.')
                print('Quitting...')
                run = False

def printMenu():

    print('-----***----- SPOTIFY TO MP3 -----***------\n')

    # Main menu operations
    print('1. Automatically Run Checks on Provided Spotify Playlist IDs')
    print('2. Assign a Source to Spotify Song')
    print('3. Create a Fully Custom Song')

    # Utility
    print('4. Edit Environment Variables')
    print('5. Exit the Program')

    print('\n-----***----- - - * ** * - - -----***------')
    # Ensure newline
    print()

def autoUpdate(self):
    # *****         MAIN SCRIPT         *****

    # Get Spotify playlist IDs & Apple Music playlist lengths
    playlistIDs = json.loads(os.environ['PLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

    # Iterate through each Spotify playlist and compare length to Apple Music lengths
    for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotify.get_playlist_length(self, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

            # Get song IDs for non-equal Spotify playlist
            print('[CACHING SONG IDS]\n')
            songIDs = spotify.get_playlist_ids(self, os.environ.get("USERNAME"), playlistIDs[playlist])

            # Get albums of missing songs
            print('[CACHING ALBUM NAMES OF MISSING SONGS]\n')
            newAlbums = spotify.get_albums_from_ids(self, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)

            # Make directories
            print('[CREATING ALBUM DIRECTORIES]\n')
            spotify.create_album_dirs((self.playlist(playlistIDs[playlist]))['name'], newAlbums)

            # Download songs & images
            print('[DOWNLOADING SONGS AND ALBUM COVERS]\n')
            spotify.download_songs_by_spotify_id(self, (self.playlist(playlistIDs[playlist]))['name'], songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

            # Move images
            print('[MOVING .JPG FILES]\n')
            spotify.move_images_to_album_dirs()

            # Update all image tags
            print('[UPDATING ID3 IMAGE TAGS]\n')
            spotify.update_img_tags()

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

def createSong():
    pass
