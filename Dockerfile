FROM python:3.10.11

ADD main.py .
ADD program.py .
ADD osScripts.py .
ADD spotifyScripts.py .

ADD .env .
ADD .cache .

RUN pip3 install yt_dlp spotipy python-requests python-dotenv

CMD ["python3", "./main.py"]
