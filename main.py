from dotenv import load_dotenv
import os
import requests

# Downloaded
import yt_dlp
from yt_dlp import YoutubeDL
import spotipy
from spotipy import SpotifyOAuth
#from spotipy.oauth2 import SpotifyClientCredentials
import json
import webbrowser
import glob

from pprint import pprint
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from mutagen.easyid3 import EasyID3  
import mutagen.id3 

import spotifyScripts
import osScripts

load_dotenv()

### Spotify Setup

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.environ.get("CLIENTID"),
                                               client_secret=os.environ.get("CLIENTSECRET"),
                                               redirect_uri="http://localhost:1234/",
                                               scope="user-library-read"))

### Apple Music Setup


### Soundcloud Setup

# tempAMLength = 76

# currentSpotifyLength = spotifyScripts.get_playlist_length(sp, '2T1a2GrAKZaAeBGw2WnBql')

# #if(tempAMLength != currentSpotifyLength):
#         #print(currentSpotifyLength - tempAMLength)

# ids = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), '2T1a2GrAKZaAeBGw2WnBql')
        
        # # ***** image extraction test code *****
        # #pprint(spotifyScripts.get_album_cover_url(sp, ids[0]))
        # osScripts.download_img('Eternal Atake', spotifyScripts.get_album_cover_url(sp, ids[0]))

        # # ***** album name extraction test code *****
        # albums = spotifyScripts.get_albums_from_ids(sp, tempAMLength, currentSpotifyLength, ids)
        #pprint(albums)

        # ***** album directory creation test code *****
        #osScripts.create_album_dir(albums)

        # ***** song download test code *****

        # ydl_opts = {
        #         'format': 'bestaudio/best',
        #         'postprocessors': [{
        #                 'key': 'FFmpegExtractAudio',
        #                 'preferredcodec': 'mp3',
        #                 'preferredquality': '192'
        #         }],
        #         'postprocessor_args': [
        #                 '-ar', '16000'
        #         ],
        #         'prefer_ffmpeg': True,
        #         'keepvideo': False
        # }

        # for id in ids:
        #         track = spotifyScripts.get_track_info(sp, id)
        #         pprint(track['name'] + ' Official Audio')
        #         searchString = track['name'] + ' Official Audio'

        #         with YoutubeDL(ydl_opts) as ydl:
        #                 video = str(ydl.extract_info(f"ytsearch:{searchString}", download= False)['entries'][0]['webpage_url'])
        #                 pprint(video)

        #                 ydl.download([video])

        #                 break

        # with YoutubeDL(ydl_opts) as ydl:
        #         ydl.download(['http://www.youtube.com/watch?v=BaW_jenozKc'])

        #osScripts.download_songs_by_spotify_id(sp, ids[tempAMLength:currentSpotifyLength])
        #pprint(ids)

        # # ***** metadata test code *****
# audio = MP3('Travis Scott - BACC.mp3', ID3=EasyID3)
# #print(audio)
# print(audio.pprint())
        
        # audiop2 = ID3('Lil Uzi Vert - Venetia [Official Audio] [hihYATpt9oo].mp3')
        # audiop2.pprint()

        # mp3Files = glob.glob("*.mp3")
        
        # for path in mp3Files:
        #         print(path)
        
        # # get position in album
# track = spotifyScripts.get_track_info(sp, ids[tempAMLength-2])
# pprint(track)
        # pprint(str(track['track_number']) + '/' + str(track['album']['total_tracks']))

        # mp3File = MP3(mp3Files[0], ID3=ID3)
        # #print(mp3File)

        # try:
        #         mp3File.add_tags()
        # except error:
        #         pass

        # mp3File.tags.add(APIC(mime='image/jpeg', type=3,desc=u'Cover',data=open('Eternal Atake.jpg', 'rb').read()))
        # mp3File.save()
        # mp3F = MP3(mp3Files[0], ID3=EasyID3)
        # print(mp3F)

        # audio2 = MP3('Lil Uzi Vert - Venetia [Official Audio] [hihYATpt9oo].mp3')
        # print(audio2.pprint())

        # mp3File2 = MP3(mp3Files[1], ID3=EasyID3)
        # print(mp3File2)

        # # identify and create string of album artists
        # albumArtists = ''
        # numArtistsInAlbum = len(track['album']['artists'])
        # for i in range(numArtistsInAlbum):
        #         if i:
        #                 albumArtists += ', '
                
        #         albumArtists += track['album']['artists'][i]['name']

        # # set album artists tag
        # mp3File['albumartist'] = albumArtists

        # print(mp3File)

        # ***** FINAL SCRIPT SETUP *****
# Get Spotify playlist IDs & Apple Music playlist lengths
playlistIDs = json.loads(os.environ['PLAYLISTS'])
AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

# Iterate through each Spotify playlist and compare length to Apple Music lengths
for playlist in range(len(playlistIDs)):

        currentSpotifyLength = spotifyScripts.get_playlist_length(sp, playlistIDs[playlist])

        if(currentSpotifyLength != AMPlaylistLengths[playlist]):

                # Get song IDs for non-equal Spotify playlist
                songIDs = spotifyScripts.get_playlist_ids(sp, os.environ.get("USERNAME"), playlistIDs[playlist])

                # Get albums of missing songs
                newAlbums = spotifyScripts.get_albums_from_ids(sp, int(AMPlaylistLengths[playlist]), currentSpotifyLength, songIDs)
                pprint(newAlbums)

                # Make directories
                osScripts.create_album_dirs((sp.playlist(playlistIDs[playlist]))['name'], newAlbums)

                # Download songs
                osScripts.download_songs_by_spotify_id(sp, songIDs, int(AMPlaylistLengths[playlist]), currentSpotifyLength)

                # Download images

                # Update Apple Music playlist lengths automatically
                AMPlaylistLengths[playlist] = currentSpotifyLength
                os.environ['AMPLAYLISTLENGTHS'] = str(AMPlaylistLengths)

                pass
        #0CdFo515yc2vcintnGYG3b     <- single uzi playlist
        #2T1a2GrAKZaAeBGw2WnBql     <- 78 song uzi playlist