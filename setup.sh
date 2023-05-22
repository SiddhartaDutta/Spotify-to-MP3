#!/bin/bash

# Setup .env file
python3 ./setup.py

# Build program image
docker build -f Dockerfile -t spotify-to-mp3 .

# Run program image
docker run -it spotify-to-mp3