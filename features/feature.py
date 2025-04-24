from pandas import DataFrame
import streamlit

class Feature:
    def __init__(self, st: streamlit, feature_name: str, enabled: bool = False):
        self.st = st
        self.enabled = enabled
        self.feature_name = feature_name
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        return df, len(df)

    def get_feature(self):
        return