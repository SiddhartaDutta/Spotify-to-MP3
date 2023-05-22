# Spotify to MP3

## Disclaimer

This project is designed to be both a learning tool and for experimental purposes only. <u>**The author takes no responsibility for damage or misfunction of any kind caused by the software in this repository.**</u> Please use both caution and common sense when using this project.

## Description

**Spotify to MP3** is a collection of scripts written and organized to help the user download their playlists in a relatively quick and organized manner. The MP3 files contain metadata in the ID3 format so that the MP3 files may be exported to a MP3 manager, such as Spotify or iTunes (although only iTunes will allow "premium" features for owned MP3 files, not Spotify) without the user having to edit metadata (files will organize themselves based on their metadata).

## Badges

## Visuals

## Usage (Running a Docker Image)

Please download the correct *.zip* file from the repository. After unzipping, place the unzipped folder where you want the downloaded music to be stored. Music is downloaded, placed in a single all-containing folder, and this folder is then placed in the same location the script was ran in. It is recommended to create a folder in your *Music* folder and place the unzipped folder in there. Run *script.sh* according to your command shell.

NOTE: System administrator permissions are required due to Docker. The script and subsequently generated Docker image will not work without administrator permissions.

Bash:
```
sudo script.sh
```

Powershell:

There is currently no Powershell support. If you have WSL on Windows, you can follow the same step as if you had Bash (above).

<details><summary>What does the script do?</summary>
When you run the script, it first asks you for some required information so that the program can access your Spotify data and know where to save downloaded MP3 files. Afterwards, it creates a *.env* file to store this data (this data can later be edited through the main menu in the program). It then creates a Docker image with the required files and deletes all the downloaded files (you can also delete the *.zip* you downloaded earlier if you have not already, it is not needed after unzipping). You are now left with none of the files related to the program except for the generated Docker image. Running the Docker image with the instructions below will always run the program.

NOTE: The setup script will not delete a single *.env* file which will be placed where the *.zip* is placed. DO NOT DELETE THIS. Deleting may prevent the Docker image from working. 
</details>

After having run the initial setup image, you can just run ***spotify-to-mp3*** for any subsequent use of the program:
```.sh
sudo docker run -it spotify-to-mp3
```

## Cloning the Project
To clone this project, you will need the following:
### Language
* [Python3](https://www.python.org/downloads/) 

Please follow the linked instructions should you not already have Python (this program utilizes Python 3.10.11)
### Modules
#### Modules to be Installed:
* [yt-dlp](https://github.com/yt-dlp/yt-dlp)

* [spotipy](https://github.com/spotipy-dev/spotipy)

* [dotenv]()

* [requests]()

Running the following command in your virtual environment (or where ever you wish to have the modules) should download all required and non-standard modules:
```.sh
pip3 install yt_dlp spotipy python-requests python-dotenv
```

#### Pre-Installed Modules (Installation should be unneeded):
* os

* glob

* json

* time

* shutil

* mutagen

## Support

## Roadmap

## Contributing

I am not currently looking for any collaborators.

## Authors and Acknowledgment

