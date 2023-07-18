"""Module for extracting song information"""
from typing import List
from spotipy.client import Spotify

class Song:
    def __init__(self, song_name: str, spotify_client: Spotify):
        """
        Represents a song and extracted information.

        Args:
            song_name: The name of the song.
            spotify_client: Spotify client instance.
        """
        self.song_name = song_name
        self.spotify_client = spotify_client
        self.song_id = self._get_song_id(self.song_name)
        self.song_info = self.spotify_client.track(self.song_id)

    def get_genres(self) -> List[str]:
        """
        Get the genres associated with the song.
        """
        return self.spotify_client.artist(self.song_info['artists'][0]['id'])['genres']

    def _get_song_id(self, song_name: str) -> str:
        """
        Get the Spotify ID of the song.

        Args:
            song_name: The name of the song.
        """
        results = self.spotify_client.search(q='track:' + song_name, type='track', limit=1)
        items = results['tracks']['items']
        if len(items) > 0:
            return items[0]['id']
        else:
            return None
