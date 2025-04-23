import pandas as pd
from pandas import DataFrame

class DFAdapter:
    def __init__(self, df: DataFrame):
        self.df = df

    def get_slider(self, start, end, feature_name) -> DataFrame:
        return self.df[(self.df[feature_name] >= start) & (self.df[feature_name] <= end)]

    def get_original_df(self) -> DataFrame:
        return pd.read_csv('spotify_songs.csv')

    def get_unique_values(self, feature_name: str) -> list:
        return list(self.df[feature_name].unique())

    def get_genres(self) -> list:
        return list(self.df['playlist_genre'].unique())

    def get_subgenres(self, genre: str) -> list:
        subgenres = self.df[self.df['playlist_genre'] == genre]['playlist_subgenre'].unique()
        return list(subgenres)

    def get_date(self, from_date = None, to_date = None) -> (DataFrame, int):
        if from_date and not to_date:
            filtered_df = self.df[self.df['track_album_release_date'] >= from_date]
        elif not from_date and to_date:
            filtered_df = self.df[self.df['track_album_release_date'] <= to_date]
        elif from_date and to_date:
            mask = (self.df['track_album_release_date'] >= from_date) & (self.df['track_album_release_date'] <= to_date)
            filtered_df = self.df[mask]
        else:
            return self.df, self.df.shape[0]
        return filtered_df, len(filtered_df)
