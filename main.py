import os
import json
import time
import dotenv
from dotenv import load_dotenv

import spotipy
from spotipy import SpotifyOAuth

import spotifyScripts
import osScripts

startTime = time.time()

load_dotenv()

### Spotify Setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))



# *****         MAIN SCRIPT         *****

# Get Spotify playlist IDs & Apple Music playlist lengths
playlistIDs = json.loads(os.environ['PLAYLISTS'])
AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

# Iterate through each Spotify playlist and compare length to Apple Music lengths
for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotifyScripts.get_playlist_length(sp, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

                # Get song IDs for non-equal Spotify playlist
                print('[CACHING SONG IDS]\n')
                songIDs = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), playlistIDs[playlist])

                # Get albums of missing songs
                print('[CACHING ALBUM NAMES OF MISSING SONGS]\n')
                newAlbums = spotifyScripts.get_albums_from_ids(sp, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)

                # Make directories
                print('[CREATING ALBUM DIRECTORIES]\n')
                osScripts.create_album_dirs((sp.playlist(playlistIDs[playlist]))['name'], newAlbums)

                # Download songs & images
                print('[DOWNLOADING SONGS AND ALBUM COVERS]\n')
                osScripts.download_songs_by_spotify_id(sp, (sp.playlist(playlistIDs[playlist]))['name'], songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

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

                print('[PLAYLIST UPDATE COMPLETE] PLAYLIST: %-*s NEW LENGTH: %s\n' % (25, str((sp.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
        else:
                print("[NO UPDATE AVAILABLE] %-*s PLAYLIST: %-*s CURRENT LENGTH: %s\n" % (4, '', 25, str((sp.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))

print('Total Runtime: ' + str(time.time() - startTime))