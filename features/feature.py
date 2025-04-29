from typing import Any

import streamlit

from app.json_handler import JsonHandler


class Feature:
    def __init__(self, st: streamlit, feature_name: str):
        self.st = st
        self.feature_name = feature_name
        self.feature_info = JsonHandler.load_features_info('data/')[feature_name]
    def show_feature(self) -> Any:
        return
