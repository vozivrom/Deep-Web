from fastapi import FastAPI
from pydantic import BaseModel
from app.domain import *
from app.json_handler import JsonHandler

app = FastAPI()
json_handler = JsonHandler()

k_max = None

class Value(BaseModel):
    name: str
    value: int



@app.put("/k_max")
def post_k_max(value: Value):
    global k_max
    k_max = value.value
    return value

@app.get("/k_max")
def get_k_max():
    return k_max

@app.put('/{feature_name}')
def save_feature(feature_name: str, df: list[dict]):
    json_handler.save_data(f'{feature_name}.json', df)

@app.get('/{feature_name}')
def get_feature(feature_name: str):
    data = json_handler.load_data(f'{feature_name}.json')
    return data