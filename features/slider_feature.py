from pandas import DataFrame

from features.feature import Feature
from app.dataframe_handler import DFHandler

class SliderFeature(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # Track Popularity and Duration in minutes

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)
        min_value = DFHandler.get_original_df()[self.feature_name].min()
        max_value = DFHandler.get_original_df()[self.feature_name].max()

        start, end = self.st.slider(
            label=self.feature_name,
            min_value=0,
            max_value=round(max_value) + 1 if self.feature_name == 'duration_in_minutes' else max_value,
            value=self.value if self.value else (round(min_value), round(max_value)),
            step=1,
            label_visibility='collapsed'
        )
        filtered_df = df[(df[self.feature_name] >= start) & (df[self.feature_name] <= end)]
        k = len(filtered_df)
        self.st.write(f'k = {k}')
        if k < k_max:
            self.st.write(filtered_df)

        df_handler = DFHandler(filtered_df)
        df_handler.put_df(self.feature_name)

        return filtered_df, k
