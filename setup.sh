#!/bin/bash

# Get current directory
CURRENTPATH=$(pwd)

# Setup .env file
python3 ./setup.py

# Build program image
docker build -f Dockerfile -t spotify-to-mp3 .

# Run program image
docker run --name spotify_to_mp3 -it --mount type=bind,src=$CURRENTPATH,target=/src spotify-to-mp3

