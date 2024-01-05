FROM python:3.10.11-alpine

RUN apk add --no-cache ffmpeg

ADD main.py .
ADD op_scripts .

ADD .env .
ADD .cache* .

#COPY requirements.txt requirements.txt
RUN pip3 install yt_dlp python-requests python-dotenv pydub ibroadcast && pip3 install spotipy --upgrade && pip3 install --upgrade yt-dlp

WORKDIR /src
CMD ["python3", "./main.py"]