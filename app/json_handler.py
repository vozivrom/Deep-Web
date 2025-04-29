import json
import os


class JsonHandler:
    @classmethod
    def save_data(cls, path: str, data: dict):
        with open(path, "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_data(cls, path: str) -> dict:
        with open(path, "r", encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def save_features_info(cls, data: dict):
        with open('../data/features_info.json', "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_features_info(cls, path: str) -> dict:
        with open(os.path.join(path, 'features_info.json'), "r", encoding='utf-8') as file:
            return json.load(file)

    @classmethod
    def save_features_params(cls, path:str, data: dict):
        with open(os.path.join(path, 'features_params.json'), "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    @classmethod
    def load_features_params(cls, path: str) -> dict:
        with open(os.path.join(path, 'features_params.json'), "r", encoding='utf-8') as file:
            return json.load(file)

