import pandas as pd
from pandas import DataFrame


class DFHandler:
    def __init__(self, df: DataFrame):
        self.df = df

    @classmethod
    def get_original_df(cls) -> DataFrame:
        return pd.read_csv('data/spotify_songs.csv')

    @classmethod
    def get_unique_values(cls, feature_name: str) -> list:
        return list(cls.get_original_df()[feature_name].unique())

    def to_json(self) -> list[dict]:
        df_json = self.df.copy()
        df_json['track_album_release_date'] = df_json['track_album_release_date'].astype(str)
        df_json = df_json.to_dict(orient="records")
        return df_json