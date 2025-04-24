from pandas import DataFrame
import numpy as np

from features.feature import Feature
from app.dataframe_handler import DFHandler

class Loudness(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)

        df_handler = DFHandler(df)
        original_df = df_handler.get_original_df()
        sorted_series = original_df[self.feature_name].sort_values()
        chunks = np.array_split(sorted_series, 4)

        quiet_normal_threshold = chunks[0].iloc[-1]
        normal_loud_threshold = chunks[2].iloc[-1]

        options = ['Quite', 'Normal', 'Loud']
        choice = self.st.pills('', options, default=self.value, selection_mode="single")

        filtered_df, k = df_handler.get_loudness(choice, quiet_normal_threshold, normal_loud_threshold)

        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)

        filtered_df_handler = DFHandler(filtered_df)
        filtered_df_handler.put_df(self.feature_name)

        return filtered_df, k
