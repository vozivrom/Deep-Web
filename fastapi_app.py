# fastapi_backend.py
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import json

from app.json_handler import JsonHandler

app = FastAPI()
json_handler = JsonHandler()

# Mount static files (HTML + JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

# Save the filters
@app.put("/features_params")
async def save_feature(request: Request):
    data = await request.json()
    features_params = {
        'track_album_release_date': data.get('track_album_release_date'),
        'playlist_genre': data.get('playlist_genre'),
        'playlist_subgenre': data.get('playlist_subgenre'),
        'track_popularity': data.get('track_popularity'),
        'duration_in_minutes': data.get('duration_in_minutes'),
        'loudness': data.get('loudness'),
        'track_artist': data.get('track_artist'),
        'track_album_name': data.get('track_album_name'),
        'track_name': data.get('track_name')
    }
    json_handler.save_features_params(features_params)
    return {"message": "Feature saved"}

@app.get("/features_params")
async def get_feature():
    return json_handler.load_features_params()

# Return filtered results
@app.get("/filtered_data")
def get_filtered_data():
    df = pd.read_csv("data/spotify_songs.csv")
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

    features_params = json_handler.load_features_params()
    features_info = json_handler.load_features_info()

    print(features_params)

    if features_params['track_album_release_date']:
        from_date, to_date = features_params['track_album_release_date']
        df = df[(df['track_album_release_date'] >= pd.to_datetime(from_date)) &
                (df['track_album_release_date'] <= pd.to_datetime(to_date))]

    if features_params['playlist_genre']:
        df = df[df['playlist_genre'].isin(features_params['playlist_genre'])]
    if features_params['playlist_subgenre']:
        df = df[df['playlist_subgenre'].isin(features_params['playlist_subgenre'])]

    if features_params['track_popularity']:
        min_pop, max_pop = features_params['track_popularity']
        df = df[(df['track_popularity'] >= min_pop) & (df['track_popularity'] <= max_pop)]

    if features_params['duration_in_minutes']:
        min_dur, max_dur = features_params['duration_in_minutes']
        df = df[(df['duration_in_minutes'] >= min_dur) & (df['duration_in_minutes'] <= max_dur)]

    if features_params['loudness']:
        if features_params['loudness'] == 'Quiet':
            df = df[df['loudness'] < features_info['loudness']['quiet_normal_threshold']]
        elif features_params['loudness'] == 'Normal':
            df = df[(df['loudness'] >= features_info['loudness']['quiet_normal_threshold']) &
                    (df['loudness'] <= features_info['loudness']['normal_loud_threshold'])]
        elif features_params['loudness'] == 'Loud':
            df = df[df['loudness'] > features_info['loudness']['normal_loud_threshold']]

    if features_params['track_artist']:
        df = df[df['track_artist'].str.contains(features_params['track_artist'], case=False, na=False, regex=False)]

    if features_params['track_album_name']:
        df = df[df['track_album_name'].str.contains(features_params['track_album_name'], case=False, na=False, regex=False)]

    if features_params['track_name']:
        df = df[df['track_name'].str.contains(features_params['track_name'], case=False, na=False, regex=False)]

    df_json = df.copy()
    df_json['track_album_release_date'] = df_json['track_album_release_date'].astype(str)
    df_json = df_json.to_dict(orient="records")
    return df_json



# @app.get("/", response_class=HTMLResponse)
# def root():
#     """Serve the frontend HTML"""
#     with open("static/index.html", "r", encoding="utf-8") as file:
#         return HTMLResponse(content=file.read())
#
# @app.put('/{feature_name}')
# def save_feature(feature_name: str, df: list[dict]):
#     json_handler.save_feature(f'{feature_name}.json', df)
#
# @app.get('/{feature_name}')
# def get_feature(feature_name: str):
#     data = json_handler.load_feature(f'{feature_name}.json')
#     return data

