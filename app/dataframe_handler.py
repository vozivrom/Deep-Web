import pandas as pd
from pandas import DataFrame
import requests

class DFHandler:
    def __init__(self, df: DataFrame):
        self.df = df

    def get_slider(self, start, end, feature_name) -> DataFrame:
        return self.df[(self.df[feature_name] >= start) & (self.df[feature_name] <= end)]

    @classmethod
    def get_original_df(cls) -> DataFrame:
        return pd.read_csv('data/spotify_songs.csv')

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

    def get_loudness(self, choice: str, quiet_normal_threshold: int, normal_loud_threshold: int) -> (DataFrame, int):
        filtered_df = self.df
        if choice == 'Quiet':
            filtered_df = self.df[self.df['loudness'] < quiet_normal_threshold]
        elif choice == 'Normal':
            filtered_df = self.df[(self.df['loudness'] >= quiet_normal_threshold) & (self.df['loudness'] <= normal_loud_threshold)]
        elif choice == 'Loud':
            filtered_df = self.df[self.df['loudness'] > normal_loud_threshold]
        k = len(filtered_df)

        return filtered_df, k

    def to_json(self) -> list[dict]:
        df_json = self.df.copy()
        df_json['track_album_release_date'] = df_json['track_album_release_date'].astype(str)
        df_json = df_json.to_dict(orient="records")
        return df_json

    def put_df(self, feature_name: str):
        df_json = self.to_json()
        requests.put(f"http://127.0.0.1:8000/{feature_name}", json=df_json)