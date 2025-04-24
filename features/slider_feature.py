from pandas import DataFrame

from features.feature import Feature
from app.dataframe_handler import DFHandler

class SliderFeature(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # Track Popularity and Duration in minutes

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

        df_handler = DFHandler(filtered_df)
        df_handler.put_df(self.feature_name)

        return filtered_df, k
