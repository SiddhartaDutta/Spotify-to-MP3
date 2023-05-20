# Spotify to MP3

## Disclaimer

This project is designed to be both a learning tool and for experimental purposes only. <u>**The author takes no responsibility for damage or misfunction of any kind caused by the software in this repository.**</u> Please use both caution and common sense when using this project.

## Description

**Spotify to MP3** is a collection of scripts written and organized to help the user download their playlists in a relatively quick and organized manner. The MP3 files contain metadata in the ID3 format so that the MP3 files may be exported to a MP3 manager, such as Spotify or iTunes (although only iTunes will allow "premium" features for owned MP3 files, not Spotify) without the user having to edit metadata (files will organize themselves based on their metadata).

## Badges

## Visuals

## Usage (Running a Docker Image)

Please get the Docker image by running the following command in your terminal:
```.sh
sudo docker pull ...
```

After pulling, please run the following command in your terminal:
```.sh
sudo docker run -it spotify-to-mp3-setup
```
This will automatically setup the required environment file and both build and run a new Docker image called ***spotify-to-mp3***.

After having run the initial setup image, you can just run ***spotify-to-mp3*** for any subsequent use of the program.

***spotify-to-mp3-setup*** may be deleted with the following command:
```.sh
sudo docker rmi $(docker images | grep 'spotify-to-mp3-setup')
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

