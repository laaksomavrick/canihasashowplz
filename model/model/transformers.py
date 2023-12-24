import community
import networkx as nx
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import LabelEncoder


class AddIsLikedAttribute(BaseEstimator, TransformerMixin):
    def __init__(self):
        super()

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X["is_liked"] = (X["rating"] >= 8).astype(bool)
        return X

class ShowUserEncoder(BaseEstimator, TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        label_encoder = LabelEncoder()
        X['user_id_encoded'] = label_encoder.fit_transform(X['user_id'])
        X['show_id_encoded'] = label_encoder.fit_transform(X['show_id'])
        return X

class DropColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop):
        self.columns_to_drop = columns_to_drop

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.drop(columns=self.columns_to_drop, errors="ignore")
        return X


class DropDuplicates(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_drop_dupes):
        self.columns_to_drop_dupes = columns_to_drop_dupes

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.drop_duplicates(subset=self.columns_to_drop_dupes)
        return X


class PivotShowIds(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.pivot(index="user_id", columns="show_id", values="is_liked").fillna(0)
        return X


class AddGraphPartitionIdAttribute(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.nn_model = NearestNeighbors(metric="cosine", algorithm="brute")
        self.pivoted = None

    def fit(self, X, y=None):
        self.pivoted = X.pivot(
            index="user_id", columns="show_id", values="is_liked"
        ).fillna(0)
        self.nn_model.fit(self.pivoted.T)

        similarities = self.nn_model.kneighbors(self.pivoted.T, return_distance=False)

        self.G = nx.Graph()

        # Add nodes to the graph
        for i in range(len(self.pivoted.T)):
            self.G.add_node(i)  # Each node represents an item/user

        # Add edges based on similarities
        for i, neighbors in enumerate(similarities):
            for neighbor in neighbors[1:]:  # Skip the first neighbor as it's itself
                self.G.add_edge(i, neighbor, weight=1)

        self.partition = community.best_partition(self.G)

        for node, cluster_id in self.partition.items():
            self.G.nodes[node]["cluster"] = cluster_id
            self.G.nodes[node]["show_index"] = node

        return self

    def transform(self, X):
        for show_idx in range(len(self.partition)):
            partition_id = self.partition[show_idx]
            show_id = self.pivoted.columns[show_idx]
            mask = X["show_id"] == show_id
            X.loc[mask, "partition_id"] = partition_id

        return X
