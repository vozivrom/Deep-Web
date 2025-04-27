from pandas import DataFrame

from features.feature import Feature
from app.dataframe_handler import DFHandler

class StringFeature(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # Track Popularity and Duration in minutes

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)
        user_input = self.st.text_input(label=self.feature_name, value=self.value, key=self.feature_name, label_visibility='collapsed')

        filtered_df = df
        if user_input:
            #  Case-insensitive
            filtered_df = df[df[self.feature_name].str.contains(user_input, case=False, na=False)]

        k = len(filtered_df)
        self.st.write(f'k = {k}')

        if k < k_max:
            self.st.write(filtered_df)

        df_handler = DFHandler(filtered_df)
        df_handler.put_df(self.feature_name)

        return filtered_df, k
