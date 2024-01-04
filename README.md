# Spotify to MP3

## Disclaimer

This project is designed to be both a learning tool and for experimental purposes only. <u>**The author takes no responsibility for damage or misfunction of any kind caused by the software in this repository.**</u> Please use both caution and common sense when using this project.

## Description

**Spotify to MP3** is a collection of scripts written and organized to help the user download their playlists in a relatively quick and organized manner. The MP3 files contain metadata in the ID3 format so that the MP3 files may be exported to an MP3 manager, such as iBroadcast, iTunes or Spotify (although Spotify does not allow "premium" features for owned MP3 files), without the user having to edit metadata.

## Badges
![LICENSE](https://img.shields.io/github/license/SiddhartaDutta/spotify-to-mp3)

## Visuals

Coming soon.

## Usage (Running a Docker Image)

**Prerequisite: Docker**

<details><summary>Installing Docker</summary>

***
Detailed instructions will come in the future. Please follow the instructions here instead: https://docs.docker.com/get-docker/
***

</details>

**Prerequisite: pip3**

<details><summary>Installing pip3</summary>

***
Please enter the following command into your terminal (if you are not sure if you have pip3, it is safe to run this command still):

```
sudo apt install python3-pip
```
***

</details>

**Prerequisite: MP3 Manager of Your Choice**

<details><summary>MP3 Managers</summary>

***
If you have an Apple device, it is highly recommended you use either iBroadcast or Apple Music as your MP3 manager.

If you have an Android device, it is highly recommended you use iBroadcast.

Spotify is **not** recommended as even with your own MP3 files, Spotify still applies non-premium rules such as limited skips and ads.

Other managers may work, those previously mentioned have just been tested with this program.
***

</details>

Please download the *.zip* file from the repository. After unzipping, place the unzipped folder where you want the downloaded music to be stored. Music is downloaded, placed in a single all-containing folder, and this folder is then placed in the same location the script was ran in. It is recommended to create a folder in your *Music* folder and place the unzipped folder in there. Run *setup.sh* according to your command shell. Follow all instructions when prompted.

***
**NOTE**: System administrator permissions are required due to Docker. The script and subsequently generated Docker image will not work without administrator permissions.

**NOTE**: If using WSL on Ubuntu 22.xx, make sure to run the following commands prior to running the script (adds missing yet required tools):
```
sudo add-apt-repository ppa:wslutilities/wslu
sudo apt update
sudo apt install wslu
```

***

Bash/WSL:
```
sudo ./setup.sh
```

If being told that script cannot run, run the follow command before trying again:
```
sudo chmod +x setup.sh
```

***

Powershell:

There is currently no Powershell support. If you have WSL on Windows, you can follow the same step as if you had Bash (above).

***

After having run the initial setup image, you can just run the ***spotify_to_mp3*** container for any subsequent use of the program:
```.sh
sudo docker start -ai spotify_to_mp3
```

## Frequently Asked Questions (For the Tool)
**How is the tool designed to be used?** 
<details><summary>Answer</summary>

***
When using iBroadcast for your music library, your songs will be added in the same order they appear when you decide to update your playlist. If you wish for iBroadcast to mirror Spotify (only when uploading initially), then you can use the tool regularly with no worry about song order specification.

When using Apple Music for your music library, it is highly recommended that when creating playlists on Spotify, you create them grouped as albums; all songs belonging to an album should be grouped chronologically together. This style of listening involves fully listening to an album at once and adding desired songs then.

Note for Apple Music: However, if you do not wish to listen to music in an album fashion, you can still easily add albums to your MP3 manager. After downloading your music, you can sort the album folders by those edited most recent. This way, all albums will be listed that need to be transferred (is beneficial when there are a large amount of albums/singles).
***

</details>

**How do I get a Spotify playlist's ID?** 
<details><summary>Answer</summary>

***
First get the share link to a playlist. The playlist ID is after the '/playlist/' to the first question mark.

Example: https://open.spotify.com/playlist/0CdFo515yc2vcintnGYG3b?si=e8f762d893c64743

The ID is **0CdFo515yc2vcintnGYG3b**
***

</details>

**How do I get a Spotify song's ID?**

<details><summary>Answer</summary>

***
First get the share link to a song. The song ID is after the '/track/' to the first question mark.

Example: https://open.spotify.com/track/4PTG3Z6ehGkBFwjybzWkR8?si=d6d587fe7439454f

The ID is **4PTG3Z6ehGkBFwjybzWkR8**
***

</details>

**How do I get a iBroadcast playlist's ID?** 
<details><summary>Answer</summary>

***
First locate the url when your playlist is open. The playlist ID follows the ID tag within the URL and prior to the apersand (&).

Example: https://media.ibroadcast.com/?view=container&container_id=######&type=playlists

The ID is **######**
***

</details>

## Cloning the Project
To clone this project, you will need the following:
### Language
* [Python3](https://www.python.org/downloads/) 

Please follow the linked instructions should you not already have Python (this program utilizes Python 3.10.11)
### Modules
#### Modules to be Installed:
* [yt-dlp](https://pypi.org/project/yt-dlp/)

* [spotipy](https://pypi.org/project/spotipy/)

* [dotenv](https://pypi.org/project/python-dotenv/)

* [requests](https://pypi.org/project/requests/)

* [pydub](https://pypi.org/project/pydub/)

* [ibroadcast](https://pypi.org/project/ibroadcast/)

Running the following command in your virtual environment (or where ever you wish to have the modules) should download all required and non-standard modules:
```.sh
pip3 install yt_dlp python-requests python-dotenv pydub ibroadcast && pip3 install spotipy --upgrade
```

#### Pre-Installed Modules (Installation should be unneeded):
* os

* glob

* json

* time

* shutil

* mutagen

You can then clone the repository with the following command:
```.sh
git clone https://github.com/SiddhartaDutta/Spotify-to-MP3.git
```

## Contributing

I am not currently looking for any collaborators.

