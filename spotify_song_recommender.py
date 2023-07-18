"""
Main module for recommending
"""
import ast
import pandas as pd

from models.clustering import perform_clustering, find_optimal_clusters
from src.song import Song
from src.genre import get_all_songs_by_genres
from src.spotify_client import SpotifyClient
from src.openai_client import OpenAIClient


class SpotifySongRecommender:
    def __init__(self):
        self.sp = SpotifyClient().get_spotify_client()
        self.openai = OpenAIClient()
        self.df = None
        self.song = None

    def _extract_songs(self, song_name, api_working=False):
        self.song = Song(song_name, self.sp)
        if api_working:
            genres = self.song.get_genres()
            self.df = get_all_songs_by_genres(genres, self.sp)

    def _cluster(self, max_clusters, clusters, path_to_data=None):
        if path_to_data:
            self.df = pd.read_csv(path_to_data)
        if clusters:
            optimal_clusters = clusters
        else:
            optimal_clusters = find_optimal_clusters(self.df, max_clusters)
        self.df = perform_clustering(self.df, optimal_clusters)

    def _recommend(self, num_songs):
        input_song_cluster = self.df[self.df["id"] == self.song.song_id][
            "cluster_label"
        ].values[0]
        similar_songs = self.df[self.df["cluster_label"] == input_song_cluster].sample(
            num_songs
        )

        similar_songs["artists"] = similar_songs["artists"].apply(ast.literal_eval)
        similar_songs["new_column"] = similar_songs.apply(
            lambda x: ", ".join(x["artists"]) + " - " + x["name"], axis=1
        )
        song_input = (
            self.song.song_info["artists"][0]["name"] + " - " + self.song.song_name
        )
        result = {
            "Input_song": song_input,
            "Recommendations": similar_songs["new_column"].tolist(),
        }
        response = self.openai.enrich_recommendation(result)
        return response

    def recommend_songs(
        self,
        song_name,
        api_working=False,
        path_to_data=None,
        num_songs=5,
        max_clusters=7,
        clusters=None,
    ):
        """
        Recommends similar songs based on an input song.

        Args:
            song_name (str): The name of the input song.
            api_working (bool): Flag indicating whether the Spotify API's rate limit
                is preventing audio feature extraction. Defaults to False.
            path_to_data (str, optional): Path to the data file containing song information. Defaults to None.
            num_songs (int, optional): Number of recommended songs to return. Defaults to 5.
            max_clusters (int, optional): The maximum number of clusters to search through
                when finding the optimal number of clusters using the elbow method.
            clusters (int, optional): Number of clusters to run Kmeans.
        """
        self._extract_songs(song_name, api_working)

        self._cluster(
            path_to_data=path_to_data, clusters=clusters, max_clusters=max_clusters
        )
        return self._recommend(num_songs)
