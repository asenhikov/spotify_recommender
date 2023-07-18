"""
Module to extract most popuar songs by given genres.
"""
from typing import List
import pandas as pd
from spotipy.client import Spotify


def get_all_songs_by_genres(genres: List[str], spotify_client: Spotify) -> pd.DataFrame:
    """
    Extract songs based on input genres and return a DataFrame.

    Args:
        genres: List of genres to extract songs from.
        spotify_client: Spotify client instance.

    Returns:
        DataFrame containing song data.

    """
    similar_songs = []
    for genre in genres:
        genre_tracks = get_tracks_by_genre(genre, spotify_client)
        similar_songs.append(genre_tracks)
    df = pd.concat(similar_songs, ignore_index=True)
    df.to_csv("song_data.csv")
    return df


def get_tracks_by_genre(
    genre: str, spotify_client: Spotify, limit: int = 50
) -> pd.DataFrame:
    """
    Extract songs from a given genre and store important attributes in DataFrame.

    Args:
        genre: Genre to extract songs from.
        spotify_client: Spotify client instance.
        limit: Maximum number of songs to extract per genre.

    Returns:
        DataFrame containing song data.

    """
    tracks = []
    offset = 0
    while len(tracks) < 900:
        results = spotify_client.search(
            q=f'genre:"{genre}"', type="track", limit=limit, offset=offset
        )
        genre_tracks = results["tracks"]["items"]
        track_ids = [track["id"] for track in genre_tracks]
        audio_features = spotify_client.audio_features(track_ids)
        for track, features in zip(genre_tracks, audio_features):
            track_info = {
                "song_name": track["name"],
                "artist": track["artists"][0]["name"],
                "song_id": track["id"],
                "acousticness": features["acousticness"],
                "danceability": features["danceability"],
                "energy": features["energy"],
                "instrumentalness": features["instrumentalness"],
                "liveness": features["liveness"],
                "loudness": features["loudness"],
                "speechiness": features["speechiness"],
                "valence": features["valence"],
                "tempo": features["tempo"],
            }
            tracks.append(track_info)
        if len(genre_tracks) < limit:
            break
        offset += limit

    df = pd.DataFrame(tracks)
    return df


