import json
import os


class JsonHandler:
    def __init__(self):
        self.data_dir = "data/"
        os.makedirs(self.data_dir, exist_ok=True)  # Ensure folder exists

    def save_data(self, path: str, data: list[dict]):
        with open(os.path.join(self.data_dir, path), "w", encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def load_data(self, path: str) -> list[dict]:
        with open(os.path.join(self.data_dir, path), "r", encoding='utf-8') as file:
            return json.load(file)

