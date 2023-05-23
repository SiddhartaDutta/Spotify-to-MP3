#!/bin/bash

# Setup .env file
python3 ./setup.py

# Build program image
docker build -f Dockerfile -t spotify-to-mp3 .

# Run program image
docker run --name spotify_to_mp3 -it spotify-to-mp3