import json
import os


class JsonHandler:
    def __init__(self):
        self.data_dir = "data/"
        os.makedirs(self.data_dir, exist_ok=True)  # Ensure folder exists

    def save_data(self, path: str, data: dict):
        with open(os.path.join(self.data_dir, path), "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def load_data(self, path: str) -> dict:
        with open(os.path.join(self.data_dir, path), "r", encoding='utf-8') as file:
            return json.load(file)

    def save_features_info(self, data: dict):
        with open('../data/features_info.json', "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def load_features_info(self) -> dict:
        with open(os.path.join(self.data_dir, 'features_info.json'), "r", encoding='utf-8') as file:
            return json.load(file)

    def save_features_params(self, data: dict):
        with open(os.path.join(self.data_dir, 'features_params.json'), "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def load_features_params(self) -> dict:
        with open(os.path.join(self.data_dir, 'features_params.json'), "r", encoding='utf-8') as file:
            return json.load(file)

