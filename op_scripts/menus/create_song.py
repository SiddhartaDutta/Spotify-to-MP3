"""
Module dedicated to creating metadata and MP3 from user provided data.
"""

import op_scripts.gen as gen
import op_scripts.spotify as spotify
import op_scripts.meta_data_frame as metaDF
import op_scripts.menus.create_album as create_album

def createSong():

    promptAns = str(input('Would you like to add a full custom album? Type \'Y\' for "Yes" or \'N\' to cancel: '))
    if(promptAns.lower() == 'y' or promptAns.lower() == 'yes'):
        create_album()
        return

    metaData = metaDF.metaDataFrame()

    run = True
    while run:

        try:

            # Get source URL
            sourceURL = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter a source URL (YouTube, SoundCloud)')
            if not sourceURL and sourceURL != 0:
                print('Operation Aborted.\n')
                break

            # Get image URL
            imgURL = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter an image source URL')
            if not imgURL and imgURL != 0:
                print('Operation Aborted.\n')
                break

            # Update album name
            metaData.albumName = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter an album title')
            albumName = [metaData.albumName]
            if not metaData.albumName and metaData.albumName != 0:
                print('Operation Aborted.\n')
                break

            # Update album release data
            metaData.releaseDate = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter the album\'s release date YEAR-MONTH-DAY (ex. 20XX-01-31)')
            if not metaData.releaseDate and metaData.releaseDate != 0:
                print('Operation Aborted.\n')
                break

            # Update album artists
            metaData.albumArtist = ''
            numOfArtists = gen.input_verification(ignoreMax= True, blankInput= True, prompt= 'Please enter the number of artists for the album')
            for n in range(numOfArtists):

                artist = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter artist #' + str(n+1) + '\'s name')
                if not artist and artist!= 0:
                    print('Operation Aborted.\n')
                    break

                if n:
                    metaData.albumArtist += ', '
            
                metaData.albumArtist += artist

            # Update song title
            metaData.title = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter the song\'s title')
            if not metaData.title and metaData.title != 0:
                print('Operation Aborted.\n')
                break

            # Update track number
            metaData.trackNumber = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter the songs\'s track number')
            if not metaData.trackNumber and metaData.trackNumber != 0:
                print('Operation Aborted.\n')
                break

            # Update song artists
            metaData.songArtist = ''
            numOfArtists = gen.input_verification(ignoreMax= True, blankInput= True, prompt= 'Please enter the number of artists for the song')
            for n in range(numOfArtists):

                artist = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter artist #' + str(n+1) + '\'s name')
                if not artist and artist!= 0:
                    print('Operation Aborted.\n')
                    break

                if n:
                    metaData.songArtist += ', '
            
                metaData.songArtist += artist

            # Update song genre
            metaData.genre = gen.input_verification(ignoreMax= True, blankInput= True, stringInput= True, prompt= 'Please enter the song\'s genre')
            if not metaData.genre and metaData.genre != 0:
                print('Operation Aborted.\n')
                break            

            # Make directories
            print('[CREATING ALBUM DIRECTORY]\n')
            spotify.create_album_dirs('', albumName)

            # Download songs & images
            print('[DOWNLOADING SONG AND ALBUM COVER]\n')
            spotify.download_img(gen.remove_slashes(metaData.albumName), imgURL)
            spotify.download_songs_by_spotify_id(self= None, IDs= None, amLength= 0, spotifyLength= 1, sourceURL= sourceURL, metaData= metaData, imgDownloaded= True)

            # Move images
            print('[MOVING .JPG FILE]\n')
            spotify.move_images_to_album_dirs()
            
            print('\n[CUSTOM MP3 FILE CREATED]\n')

            # Request for another song
            promptAns = str(input('Would you like to add another song? Type \'Y\' for "Yes" or \'N\' to cancel: '))
            if(promptAns.lower() == 'n' or promptAns.lower() == 'no'):
                run = False

            print()

            # Update all image tags
            print('[UPDATING ID3 IMAGE TAGS]\n')
            spotify.update_img_tags()

        except:
            print('[ERROR] OPERATION FAILED (Invalid Song ID and/or Invalid Source URL). The operation will be aborted.\n')
            print()
            run = False
