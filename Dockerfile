FROM python:3.10.11-alpine

RUN apk add --no-cache ffmpeg

ADD setup.py .

ADD main.py .
ADD op_scripts .

ADD LICENSE .

RUN pip3 install yt_dlp python-requests python-dotenv pydub ibroadcast tqdm && pip3 install spotipy --upgrade && pip3 install --upgrade yt-dlp

WORKDIR /src
CMD ["python3", "./main.py"]