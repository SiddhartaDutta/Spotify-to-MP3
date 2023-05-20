#!/bin/bash

# Setup .env file
python3 ./setup.py

# Build program image
sudo docker build -f Dockerfile.program -t spotify-to-mp3 .

# Run program image
python3 ./main.py