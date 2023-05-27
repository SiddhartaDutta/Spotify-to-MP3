FROM python:3.10.11-alpine

RUN apk add --no-cache ffmpeg

ADD main.py .
ADD program.py .
ADD osScripts.py .
ADD spotifyScripts.py .

ADD .env .

#COPY requirements.txt requirements.txt
RUN pip3 install yt_dlp spotipy python-requests python-dotenv

WORKDIR /src
CMD ["python3", "./main.py"]