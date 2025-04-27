from typing import Any

from pandas import DataFrame
import streamlit
import json

class Feature:
    def __init__(self, st: streamlit, feature_name: str, value: Any = None, enabled: bool = False):
        self.st = st
        self.value = value
        self.feature_name = feature_name
        self.enabled = enabled
        # with open('../features_params.json', "r", encoding='utf-8') as file:
        #     features_params = json.load(file)

        self.value = value
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        return df, len(df)

    def get_feature(self):
        return