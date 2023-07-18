import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

    def get_spotify_client(self) -> spotipy.Spotify:
        """
        Get a Spotify client instance using the provided credentials.

        Returns:
            Spotify client instance.

        """
        client_credentials = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        return spotipy.Spotify(client_credentials_manager=client_credentials)

