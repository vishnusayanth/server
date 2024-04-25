import requests
import json
import logging
from .config import SPOTIFY_TOKEN_URL, SPOTIFY_ID, SPOTIFY_SECRET


class Spotify:
    CLIENT_ID = SPOTIFY_ID
    CLIENT_SECRET = SPOTIFY_SECRET

    grant_type = 'client_credentials'
    body_params = {'grant_type': grant_type}

    def get_credentials(self):
        return self.CLIENT_ID, self.CLIENT_SECRET

    def get_headers(self):
        url = SPOTIFY_TOKEN_URL
        response = requests.post(
            url, data=self.body_params, auth=self.get_credentials())
        token_raw = json.loads(response.text)
        token = token_raw["access_token"]
        return {"Authorization": f"Bearer {token}"}


class SpotifyResult:
    def __init__(self, name, url):
        self.name = name
        self.url = str(url).replace('/', '+')


class SpotifyPlaylist:
    def __init__(self, name, iframe_url, image):
        self.name = name
        self.iframe_url = str(iframe_url).replace('/', '+')
        self.image = image


class GoogleNewsContent:
    def __init__(self, content, url, image):
        self.content = content
        self.url = url
        self.image = image

    def tojson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class DjangoAppLogger:
    def __init__(self, location):
        self.logger = logging.getLogger(location)

    def write_to_console(self, message,traceback, extra_message=None):
        if extra_message is not None:
            message += ' | Extra msg : ' + extra_message
        print(message)
        print(traceback.format_exc())
