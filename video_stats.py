import requests
import json

import os
from dotenv import load_dotenv


load_dotenv(dotenv_path = "./.env")


API_KEY = os.getenv("API_KEY")


channel_handle = "MrBeast"
#API_KEY = "AIzaSyDaTtT3mmREhY-EUltgT7TL_FmopqhhzDY"

def get_playlist_id():

    try:
        url = f"https://youtube.googleapis.com/youtube/v3/channels?part=ContentDetails&forHandle={channel_handle}&key={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

       
        channel_items=data["items"][0]
        channel_playlistID=channel_items["contentDetails"]["relatedPlaylists"]["uploads"]
        print(channel_playlistID)
        return channel_playlistID

    except requests.exceptions.RequestException as e:
        raise e
    

if __name__  == "__main__":
        get_playlist_id()
        