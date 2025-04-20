import pandas as pd
from pandas import DataFrame

class CSVAdapter:
    def __init__(self, df: DataFrame):
        self.df = df

    def get_unique_values(self, column_name: str) -> list:
        return list(self.df[column_name].unique())

    def get_genres(self) -> list:
        return list(self.df['playlist_genre'].unique())

    def get_subgenres(self, genre: str) -> list:
        subgenres = self.df[self.df['playlist_genre'] == genre]['playlist_subgenre'].unique()
        return list(subgenres)