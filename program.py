import os
import json
import dotenv

import osScripts
import spotifyScripts

def run(self):

    run = True

    while run:

        printMenu()

        userInput = inputVerification(5)

        match userInput:
            case 1:
                autoUpdate(self)
            case 2:
                sourceAndSpotify(self)
            case 3:
                createSong()
            case 4:
                editEnvVars()
            case 5:
                print('Quitting...\n')
                run = False
            case _:
                print('[ERROR] Unexpected verified input. Please publish an issue on GitHub. The program will quit now.')
                print('Quitting...')
                run = False

def inputVerification(maxCount, ignoreMax = False, blankInput = False, prompt = 'Please input selection'):
    userIn = None
     
    while userIn is None:
        try:
            if not blankInput:
                userIn = int(input(prompt + ': '))
            else:
                userIn = int(input(prompt + ' (leave blank to cancel): '))

            if userIn > maxCount and not ignoreMax:
                #userIn = None
                raise ValueError()
            
        except ValueError:
            
             if blankInput and not userIn and userIn != 0:
                return userIn
             
             userIn = None
             print('Invalid Input.')

    print()
    return userIn  

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

def createSong():
    pass

def editEnvVars():

    while True:
        print('-----***--***--- SETTINGS ---***--***------\n')

        print("Please enter the number of the variable you wish to edit:")
        print("1. Spotify Username")
        print("2. Spotify Client ID")
        print("3. Spotify Client Secret")
        print("4. Playlist Currently Downloaded Counts")
        print("5. Spotify Playlist IDs")
        print("6. Back to Main Menu")

        print('\n-----***----- - - * ** * - - -----***------\n')

        userInput = inputVerification(6)

        match userInput:
            case 1:     # Change Spotify username
                print('Current Spotify username: ' + str(os.environ.get('USERNAME')))
                print(str(os.environ.get('USERNAME')))
                inputStr = input('Please enter a new Spotify username to use (leave blank to cancel): ')

                if len(inputStr):
                    os.environ['USERNAME'] = inputStr
                    dotenv.set_key(dotenv.find_dotenv(), "USERNAME", os.environ['USERNAME'])
                    print('Saved.\n')

                else:
                    print('Operation Aborted.\n')
            
            case 2:     # Change Client ID
                print('Current Spotify Client ID: ' + str(os.environ.get('CLIENTID')))
                inputStr = input('Please input a new Spotify Client ID to use (leave blank to cancel): ')

                if len(inputStr):
                    os.environ['CLIENTID'] = inputStr
                    dotenv.set_key(dotenv.find_dotenv(), "CLIENTID", os.environ['CLIENTID'])
                    print('Saved.\n')

                else:
                    print('Operation Aborted.\n')
            
            case 3:     # Change Client Secret
                print('Current Spotify Client Secret: ' + str(os.environ.get('CLIENTSECRET')))
                inputStr = input('Please enter a new Spotify Client Secret to use (leave blank to cancel): ')

                if len(inputStr):
                    os.environ['CLIENTSECRET'] = inputStr
                    dotenv.set_key(dotenv.find_dotenv(), "CLIENTSECRET", os.environ['CLIENTSECRET'])
                    print('Saved.\n')

                else:
                    print('Operation Aborted.\n')
            
            case 4:     # Change Download Counts
                print('Current Playlist IDs and Download Count: ')
                playlistIDs = json.loads(os.environ['PLAYLISTS'])
                AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

                # Print all playlists and counts
                for playlist in range(len(playlistIDs)):
                    print('\t' + str(playlist + 1) + '. ' + str(playlistIDs[playlist]) + ': ' + str(AMPlaylistLengths[playlist]))

                # Get playlist to change
                print()
                userSelect = inputVerification(len(playlistIDs), blankInput= True, prompt= 'Please enter a playlist number')

                if not userSelect and userSelect != 0:

                    print('Operation Aborted.\n')

                else:

                    newLength = str(input('Please enter new playlist length (leave blank to cancel): '))

                    if not newLength and newLength != 0:

                        print('Operation Aborted.\n')

                    else:
                        
                        AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])
                        
                        AMPlaylistLengths[userSelect - 1] = newLength
                        
                        # Convert list to strings
                        newStr = '['
                        for entry in range(len(AMPlaylistLengths)):
                                tempStr = str(AMPlaylistLengths[entry])
                                tempStr = '"' + tempStr + '",'
                                newStr += tempStr
                        newStr = newStr[:len(newStr)-1] + ']'
                        os.environ['AMPLAYLISTLENGTHS'] = str(newStr)
                        dotenv.set_key(dotenv.find_dotenv(), "AMPLAYLISTLENGTHS", os.environ['AMPLAYLISTLENGTHS'])

                        print('Saved.\n')

            case 5:     # Edit Spotify playlist IDs
                print('Current Playlist IDs and Download Count: ')
                playlistIDs = json.loads(os.environ['PLAYLISTS'])
                AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

                # Print all playlists and counts
                for playlist in range(len(playlistIDs)):
                    print('\t' + str(playlist + 1) + '. ' + str(playlistIDs[playlist]) + ': ' + str(AMPlaylistLengths[playlist]))

                # Print 2 additional options
                print('\t' + str(len(playlistIDs) + 1) + '. Add playlist')
                print('\t' + str(len(playlistIDs) + 2) + '. Remove playlist')   

                print()
                userSelect = inputVerification(len(playlistIDs) + 2, blankInput= True)

                if not userSelect and userSelect != 0:

                    print('Operation Aborted.\n')

                else:

                    if len(playlistIDs) + 1:        # Add Playlist
                        newID = str(input('Please enter new playlist ID (leave blank to cancel): '))

                        if not newID and newID != 0:
                            print('Operation Aborted.\n')

                        else:
                            print()
                            newCount = str(input('Please enter new playlist length (leave blank to cancel): '))

                            if not newCount and newCount != 0:
                                print('Operation Aborted.\n')
                            
                            else:
                                if(len(newCount)):
                                    playlistIDs = json.loads(os.environ['PLAYLISTS'])
                                    AMPlaylistLengths = json.loads(os.environ['AMPLAYLISTLENGTHS'])

                                    playlistIDs.append(newID)
                                    AMPlaylistLengths.append(newCount)

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
                                    if len(playlistIDs) > 0:
                                        playlistLengthStr = playlistLengthStr[:len(playlistLengthStr)-1] + ']'
                                        playlistIDStr = playlistIDStr[:len(playlistIDStr)-1] + ']'

                                    # Write to env file
                                    os.environ['PLAYLISTS'] = playlistIDStr
                                    dotenv.set_key(dotenv.find_dotenv(), 'PLAYLISTS', os.environ['PLAYLISTS'])

                                    os.environ['AMPLAYLISTLENGTHS'] = playlistLengthStr
                                    dotenv.set_key(dotenv.find_dotenv(), 'AMPLAYLISTLENGTHS', os.environ['AMPLAYLISTLENGTHS'])

                                    print('Saved.\n')



                    elif len(playlistIDs) + 2:      # Remove playlist
                        pass

                    else:                           # Update playlist ID
                        pass


            case 6:
                break

            case _:
                print('[ERROR] Unexpected verified input. Please publish an issue on GitHub. The program will quit now.')
                print('Quitting...')
                break
