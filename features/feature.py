from typing import Any

from pandas import DataFrame
import streamlit

class Feature:
    def __init__(self, st: streamlit, feature_name: str, value: Any = None, enabled: bool = False):
        self.st = st
        self.value = value
        self.feature_name = feature_name
        self.enabled = enabled
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        return df, len(df)

    def get_feature(self):
        return