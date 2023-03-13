import os
import json
import dotenv
from dotenv import load_dotenv

import spotipy
from spotipy import SpotifyOAuth

import spotifyScripts
import osScripts

load_dotenv()

### Spotify Setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

# tempAMLength = 76
# currentSpotifyLength = spotifyScripts.get_playlist_length(sp, '2T1a2GrAKZaAeBGw2WnBql')
# ids = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), '2T1a2GrAKZaAeBGw2WnBql')
# track = spotifyScripts.get_track_info(sp, ids[tempAMLength-2])
# pprint(track)

# *****         MAIN SCRIPT         *****

# Get Spotify playlist IDs & Apple Music playlist lengths
playlistIDs = json.loads(os.environ['PLAYLISTS'])
AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

# Iterate through each Spotify playlist and compare length to Apple Music lengths
for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotifyScripts.get_playlist_length(sp, playlistIDs[playlist])

        if(currentSpotifyLength != int(AMPlaylistLengths[playlist])):

                # Get song IDs for non-equal Spotify playlist
                songIDs = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), playlistIDs[playlist])

                # Get albums of missing songs
                newAlbums = spotifyScripts.get_albums_from_ids(sp, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)
                #newAlbumImgURLs = spotifyScripts.get_album_cover_url(sp, ids[0])
                #pprint(newAlbums)

                # Make directories
                osScripts.create_album_dirs((sp.playlist(playlistIDs[playlist]))['name'], newAlbums)

                # Download songs
                osScripts.download_songs_by_spotify_id(sp, (sp.playlist(playlistIDs[playlist]))['name'], songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

                # Download images

                # Update Apple Music playlist lengths automatically
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

        else:
                print("[NO UPDATE AVAILABLE] PLAYLIST: %-*s CURRENT LENGTH: %s" % (25, str((sp.playlist(playlistIDs[playlist]))['name']), str(AMPlaylistLengths[playlist])))
