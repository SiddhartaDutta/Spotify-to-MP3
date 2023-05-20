import json
import dotenv
from dotenv import load_dotenv
from time import sleep

def initialSetup():

    print("The following will setup Spotify-to-MP3 for you.")
    sleep(3)
    print("Please enter the information as requested...")
    sleep(3)

    # edit env file
    load_dotenv()

    with open(".env", "w") as envFile:
        envFile.write("USERNAME=\nCLIENTID=")


    print("here")
    pass

initialSetup()