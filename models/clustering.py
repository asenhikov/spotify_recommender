"""
Module for data processing and clustering.
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

cols_for_model = ['valence',  'acousticness', 'danceability', 'duration_ms',
       'energy', 'instrumentalness', 'key', 'liveness', 'loudness',
        'popularity', 'speechiness', 'tempo']

class DataTransformer:
    """
    Class to extract columns used for clustering and apply scaling.
    """
    def __init__(self):
        self.scaler = StandardScaler()

    def transform(self, features: np.ndarray) -> np.ndarray:
        """
        Apply feature scaling and dimensionality reduction to the features.

        Args:
            features: The input features to be transformed.

        Returns:
            The transformed features.

        """
        features = features[cols_for_model]
        scaled_features = self.scaler.fit_transform(features)
        
        return scaled_features



class Clusterer:
    def __init__(self):
        self.kmeans = KMeans()

    def cluster(self, features: np.ndarray, num_clusters: int) -> np.ndarray:
        """
        Perform clustering on the features.

        Args:
            features: The input features to be clustered.
            num_clusters: The number of clusters.

        Returns:
            The cluster labels.

        """
        self.kmeans.set_params(n_clusters=num_clusters,n_init="auto", random_state=42)
        self.kmeans.fit(features)
        return self.kmeans.labels_

    def find_optimal_clusters(self, features: np.ndarray, max_clusters: int) -> int:
        """
        Find the optimal number of clusters using the elbow method.

        Args:
            features: The input features
            max_clusters: The maximum number of clusters
        """
        distortions = []
        for k in range(1, max_clusters + 1):
            self.kmeans.set_params(n_clusters=k, random_state=42)
            self.kmeans.fit(features)
            distortions.append(self.kmeans.inertia_)
        optimal_clusters = np.argmin(distortions) + 1

        return optimal_clusters

def perform_clustering(df: pd.DataFrame, num_clusters: int) -> pd.DataFrame:
    """
    Performs clustering on a DataFrame and adds cluster labels to it

    Args:
        df (pd.DataFrame): The DataFrame for clustering
        num_clusters (int): The number of clusters to create.

    Returns:
        The input df with 'cluster_label' column
    """

    transformer = DataTransformer()
    transformed_features = transformer.transform(df)

    clusterer = Clusterer()
    cluster_labels = clusterer.cluster(transformed_features, num_clusters)

    df['cluster_label'] = cluster_labels
    return df


def find_optimal_clusters(df: pd.DataFrame, max_clusters: int) -> int:
    """
    Finds the optimal number of clusters for a given df

    Args:
        df (pd.DataFrame): The DataFrame for clustering
        max_clusters (int): The maximum number of clusters to consider
    """

    transformer = DataTransformer()
    transformed_features = transformer.transform(df)

    clusterer = Clusterer()
    optimal_clusters = clusterer.find_optimal_clusters(transformed_features, max_clusters)

    return optimal_clusters