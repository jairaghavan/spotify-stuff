import requests
import os
from dotenv import load_dotenv, set_key
from pathlib import Path

ENV_PATH = Path('./.env')
load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TOKEN = os.getenv('TOKEN')

api_url = "https://api.spotify.com"
token_url = "https://accounts.spotify.com/api/token"

def refresh_token():
    r = requests.post(token_url, 
    headers={
        "Content-Type": "application/x-www-form-urlencoded"
    }, 
    data={
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    })
    TOKEN = r.json()["access_token"]
    set_key(ENV_PATH, "TOKEN", TOKEN)


# send a request to get a playlist (using my march 25 playlist for now)
r = requests.get(f"{api_url}/v1/playlists/6F0Vbgsw6CuBnrGW16Us90", headers={ "Authorization": f"Bearer {TOKEN}"})

match r.status_code:
    case 200:
        res = r.json()
        tracks = res["tracks"]["items"]

        for t in tracks:
            print(t["track"]["name"])

    case 401:
        refresh_token()
    case _:
        print(r.json()["error"]["message"])
