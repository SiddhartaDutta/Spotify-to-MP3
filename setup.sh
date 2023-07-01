#!/bin/bash

# Get current directory
CURRENTPATH=$(pwd)

# Get user who ran script
CURRENTUSER=${SUDO_USER}

# Setup .env file
echo "here"
pip3 install spotipy python-dotenv
echo "here2"
python3 ./setup.py

# Build program image
docker build -f Dockerfile -t spotify-to-mp3 .

# Delete downloaded files
rm main.py
rm osScripts.py
rm program.py
rm setup.py
rm setup.sh
rm spotifyScripts

rm LICENSE
rm Dockerfile

# Delete created files
rm .env
rm .cache

rm -rf .__pycache__/

# Run program image
docker run --name spotify_to_mp3 -it --mount type=bind,src=$CURRENTPATH,target=/src spotify-to-mp3

