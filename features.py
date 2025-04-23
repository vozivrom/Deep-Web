import pandas as pd
import numpy as np
from pandas import DataFrame
import streamlit

from dataframe_adapter import DFAdapter

class Feature:
    def __init__(self, st: streamlit, df_adapter: DFAdapter, feature_name: str, enabled: bool = False):
        self.st = st
        self.df_adapter = df_adapter
        self.enabled = enabled
        self.feature_name = feature_name
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        return df, len(df)


class TrackAlbumReleaseDate(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # self.st.write(f'{self.feature_name} {k}')
        if k < k_max:
            return df, k

        self.st.markdown('<div class="param_header">Track release date</div>', unsafe_allow_html=True)
        col1, col2 = self.st.columns(2)

        min_date = df['track_album_release_date'].min()
        max_date = df['track_album_release_date'].max()
        with col1:
            from_date = pd.to_datetime(self.st.date_input(label='From date', value=None,
                                                          min_value=min_date, max_value=max_date))

        with col2:
            to_date = pd.to_datetime(self.st.date_input(label='To date', value=None,
                                                        min_value=from_date, max_value=max_date))

        filtered_df, k = self.df_adapter.get_date(from_date, to_date)

        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)

        return filtered_df, k

class PlaylistGenre(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # self.st.write(f'{self.feature_name} {k}')
        # # GENRES
        if k < k_max:
            return df, k

        self.st.markdown('<div class="param_header">Playlist genres</div>', unsafe_allow_html=True)
        genres_choice = self.st.multiselect(
            label='',
            options=list(df['playlist_genre'].unique()),
            default=[]
        )
        filtered_df = df
        if genres_choice:
            filtered_df = df[df['playlist_genre'].isin(genres_choice)]
            k = len(filtered_df)
            self.st.write(f'k = {k}')

            if k < k_max:
                self.st.write(filtered_df)
            elif self.st.session_state.get('playlist_subgenre'):
                # SUBGENRES
                self.st.markdown('<div class="param_header">Playlist subgenres</div>', unsafe_allow_html=True)
                subgenres = []

                for _ in genres_choice:
                    subgenres += list(filtered_df['playlist_subgenre'].unique())

                sub_genres_choice = self.st.multiselect(
                    label='',
                    options=subgenres,
                    default=[]
                )

                if sub_genres_choice:
                    filtered_df = filtered_df[filtered_df['playlist_subgenre'].isin(sub_genres_choice)]
                    k = len(filtered_df)
                    self.st.write(f'k = {k}')
                    if k < k_max:
                        self.st.write(filtered_df)
                return filtered_df, len(filtered_df)

        # self.st.write(filtered_df)
        return filtered_df, len(filtered_df)

class SliderFeature(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # Track Popularity and Duration in minutes

        # self.st.write(f'{self.feature_name} {k}')
        if k < k_max:
            return df, k

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)
        min_value = df[self.feature_name].min()
        max_value = df[self.feature_name].max()

        if min_value == max_value:
            self.st.write(f'k = {k}')
            return df, k

        start, end = self.st.slider(
            label='',
            min_value=min_value,
            max_value=max_value,
            value=(min_value, max_value),
            step=0.25 if self.feature_name == 'duration_in_minutes' else 1
        )
        filtered_df = df[(df[self.feature_name] >= start) & (df[self.feature_name] <= end)]
        k = len(filtered_df)
        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)
        return filtered_df, k

class Loudness(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # self.st.write(f'{self.feature_name} {k}')
        if k < k_max:
            return df, k

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)

        original_df = self.df_adapter.get_original_df()
        sorted_series = original_df[self.feature_name].sort_values()
        chunks = np.array_split(sorted_series, 4)

        quiet_normal_threshold = chunks[0].iloc[-1]
        normal_loud_threshold = chunks[2].iloc[-1]

        options = ['Quite', 'Normal', 'Loud']
        selection = self.st.pills("Loudness", options, selection_mode="single")

        filtered_df = df
        if selection == 'Quite':
            filtered_df = df[df['loudness'] <= quiet_normal_threshold]
        elif selection == 'Normal':
            filtered_df = df[(df['loudness'] >= quiet_normal_threshold) & (df['loudness'] <= normal_loud_threshold)]
        elif selection == 'Loud':
            filtered_df = df[df['loudness'] >= normal_loud_threshold]
        k = len(filtered_df)
        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)

        return filtered_df, k

class StringFeature(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # Track Popularity and Duration in minutes
        # self.st.write(f'{self.feature_name} {k}')
        if k < k_max:
            return df, k

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)
        user_input = self.st.text_input(f"Search by {feature_name.lower()}:")

        filtered_df = df
        if user_input:
            #  Case-insensitive
            filtered_df = df[df[self.feature_name].str.contains(user_input, case=False, na=False)]

        k = len(filtered_df)
        self.st.write(f'k = {k}')

        if k < k_max:
            self.st.write(filtered_df)

        return filtered_df, k
