"""
Module dedicated to using song metadata from Spotify and a user provided source.
"""

import op_scripts.gen as gen
import op_scripts.spotify as spotify

def spotifyBase(self):

    run = True
    while run:

        try:
            songID = []
            songID.append(gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter a song\'s ID'))

            if not songID and songID != 0:
                print('Operation Aborted.\n')
                break

            sourceURL = gen.input_verification(ignoreMax= True, blankInput= True,stringInput= True, prompt= 'Please enter a source URL (YouTube, SoundCloud)')

            if not sourceURL and sourceURL != 0:
                print('Operation Aborted.\n')
                break
            
            # Get albums of missing songs
            print('[CACHING ALBUM NAMES OF MISSING SONG]\n')
            newAlbums = spotify.get_albums_from_ids(self, 0, 1, songID)

            # Make directories
            print('[CREATING ALBUM DIRECTORIES]\n')
            spotify.create_album_dirs('', newAlbums)

            # Download songs & images
            print('[DOWNLOADING SONG AND ALBUM COVER]\n')
            spotify.download_songs_by_spotify_id(self, songID, 0, 1, sourceURL)

            # Move images
            print('[MOVING .JPG FILE]\n')
            updatedAlbums = spotify.move_images_to_album_dirs()

            # Update all image tags
            print('[UPDATING ID3 IMAGE TAGS]\n')
            spotify.update_img_tags(upd)
            
            print('[CUSTOM MP3 FILE CREATED]\n')

            # Request for another song
            promptAns = str(input('Would you like to add another song? Type \'Y\' for "Yes" or \'N\' to cancel: '))
            if(promptAns.lower() == 'n' or promptAns.lower() == 'no'):
                run = False

            print()
        except:
            print('[ERROR] OPERATION FAILED (Invalid Song ID and/or Invalid Source URL). The operation will be aborted.\n')
            run = False

    print()