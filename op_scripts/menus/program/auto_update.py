"""
Module dedicated to automatically running playlist for updates.
"""

import os
import json
import dotenv
import threading
from tqdm import tqdm

import op_scripts.spotify as spotify
import op_scripts.ibroadcast as ibroadcast
from op_scripts.gen import loading_screen, prnt

def autoUpdate(self):

    # Get Spotify playlist IDs & Apple Music playlist lengths
    playlistIDs = json.loads(os.environ['SPOTIFYPLAYLISTS'])
    AMPlaylistLengths = json.loads(os.environ['DOWNLOADCOUNTS'])
    iBroadcastIDs = json.loads(os.environ['IBROADCASTPLAYLISTS'])

    if len(playlistIDs) == 0:
        print('[UPDATE] No playlists available. Please add playlists from the advanced menu.\n')
        return

    # Iterate through each Spotify playlist and compare length to downloaded counts
    for playlist in tqdm(range(len(playlistIDs)), desc= 'Check Playlists', disable= (os.environ.get('DEBUGMODE') == 'True')):

        currentSpotifyLength = spotify.get_playlist_length(self, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

            # Get song IDs for non-equal Spotify playlist
            prnt('[CACHING SONG IDS]\n')
            songIDs = spotify.get_playlist_ids(self, os.environ.get("USERNAME"), playlistIDs[playlist])

            # Get albums of missing songs
            prnt('[CACHING ALBUM NAMES OF MISSING SONGS]\n')
            newAlbums = spotify.get_albums_from_ids(self, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)

            # Make directories
            prnt('[CREATING ALBUM DIRECTORIES]\n')
            spotify.create_album_dirs((self.playlist(playlistIDs[playlist]))['name'], newAlbums)

            # Download songs & images AND record new file paths
            prnt('[DOWNLOADING SONGS AND ALBUM COVERS]\n')
            newFiles = spotify.download_songs_by_spotify_id(self,  songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

            # Move images
            prnt('[MOVING .JPG FILES]\n')
            spotify.move_images_to_album_dirs()

            # Update all image tags
            prnt('[UPDATING ID3 IMAGE TAGS]\n')
            spotify.update_img_tags()

            # Update iBroadcast if flagged
            if os.environ.get("UPDATEIBROADCAST") == 'True':
                prnt('[UPDATING iBROADCAST]\n')
                ibroadcast.upload_new(newFiles, iBroadcastIDs[playlist])

            # Update Apple Music playlist lengths automatically
            prnt('[UPDATING ENVIRONMENT VARIABLES]\n')
            AMPlaylistLengths[playlist] = currentSpotifyLength
                    # Convert list to strings
            newStr = '['
            for entry in range(len(AMPlaylistLengths)):
                    tempStr = str(AMPlaylistLengths[entry])
                    tempStr = '"' + tempStr + '",'
                    newStr += tempStr
            newStr = newStr[:len(newStr)-1] + ']'
            os.environ['DOWNLOADCOUNTS'] = str(newStr)
            dotenv.set_key(dotenv.find_dotenv(), "DOWNLOADCOUNTS", os.environ['DOWNLOADCOUNTS'])

            prnt('[PLAYLIST UPDATE COMPLETE] PLAYLIST: %-*s NEW LENGTH: %s\n' % (25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
        else:
            prnt("[NO UPDATE AVAILABLE] %-*s PLAYLIST: %-*s CURRENT LENGTH: %s\n" % (4, '', 25, str((self.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
