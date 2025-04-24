import pandas as pd
from pandas import DataFrame
import numpy as np
import requests

from features.feature import Feature
from app.dataframe_handler import DFHandler

class TrackAlbumReleaseDate(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        self.st.markdown('<div class="param_header">Track release date</div>', unsafe_allow_html=True)
        col1, col2 = self.st.columns(2)

        min_date = df['track_album_release_date'].min()
        max_date = df['track_album_release_date'].max()
        with col1:
            from_date = pd.to_datetime(self.st.date_input(label='From date', value=self.value[0],
                                                          min_value=min_date, max_value=max_date))

        with col2:
            to_date = pd.to_datetime(self.st.date_input(label='To date', value=self.value[1],
                                                        min_value=from_date, max_value=max_date))
        df_handler = DFHandler(df)
        filtered_df, k = df_handler.get_date(from_date, to_date)

        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)

        filtered_df_handler = DFHandler(filtered_df)
        filtered_df_handler.put_df(self.feature_name)

        return filtered_df, k
    