FROM python:3.10.11-alpine

RUN apk add --no-cache ffmpeg

ADD main.py .
ADD program.py .
ADD op_scripts .

ADD .env .
ADD .cache* .

#COPY requirements.txt requirements.txt
RUN pip3 install yt_dlp python-requests python-dotenv pydub && pip3 install spotipy --upgrade

WORKDIR /src
CMD ["python3", "./main.py"]