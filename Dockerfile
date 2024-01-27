FROM python:3.10.11-alpine

RUN apk add --no-cache ffmpeg

ADD setup.py src/

ADD main.py src/
ADD op_scripts src/op_scripts/

ADD LICENSE src/

RUN pip3 install yt_dlp python-requests python-dotenv pydub ibroadcast tqdm && pip3 install spotipy --upgrade && pip3 install --upgrade yt-dlp

WORKDIR /src
CMD ["python3", "main.py"]