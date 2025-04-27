import pandas as pd
from json_handler import JsonHandler
import numpy as np
import json

def save_features_info():
    df = pd.read_csv('../data/spotify_songs.csv')
    df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

    sorted_series = df['loudness'].sort_values()
    chunks = np.array_split(sorted_series, 4)

    quiet_normal_threshold = chunks[0].iloc[-1]
    normal_loud_threshold = chunks[2].iloc[-1]

    features_data = {'track_album_release_date': {'min': str(df['track_album_release_date'].min()),
                                                  'max': str(df['track_album_release_date'].max())},
                     'playlist_genre':           df['playlist_genre'].unique().tolist(),
                     'playlist_subgenre':        df['playlist_subgenre'].unique().tolist(),
                     'track_popularity':         {'min': df['track_popularity'].min().item(),
                                                  'max': df['track_popularity'].max().item()},
                     'duration_in_minutes':      {'min': df['duration_in_minutes'].min().item(),
                                                  'max': df['duration_in_minutes'].max().item()},
                     'loudness':                 {'quiet_normal_threshold': quiet_normal_threshold,
                                                  'normal_loud_threshold': normal_loud_threshold},
                     'track_artist':             df['track_artist'].unique().tolist(),
                     'track_album_name':         df['track_album_name'].unique().tolist(),
                     'track_name':               df['track_name'].unique().tolist()}
    json_handler = JsonHandler()
    json_handler.save_features_info(features_data)

def get_values(feature: str) -> list:
    with open('../data/features_info.json', "r", encoding='utf-8') as file:
        features_info = json.load(file)

    if isinstance(features_info[feature], list):
        return features_info[feature]
    elif feature == 'loudness':
        return ['Quiet', 'Normal', 'Loud']
    elif isinstance(features_info[feature], dict):
        min_value = features_info[feature]['min']
        max_value = features_info[feature]['max']
        if feature == 'track_album_release_date':
            max_value = pd.to_datetime(max_value) + pd.DateOffset(years=1)
            year_start_dates = pd.date_range(start=min_value, end=max_value, freq=pd.offsets.YearBegin(2))  # 'YS' = Year Start

            date_combinations = []
            for i in range(len(year_start_dates)):
                # for j in range(i + 1, len(year_start_dates)):
                if i == len(year_start_dates) - 1:
                    break
                start_date = year_start_dates[i]
                end_date = year_start_dates[i + 1]
                date_combinations.append((str(start_date), str(end_date)))
            return date_combinations

            # print(date_combinations)
        # slider features
        elif feature == 'track_popularity' or feature == 'duration_in_minutes':
            if feature == 'duration_in_minutes':
                max_value = round(max_value) + 1
            min_value = round(min_value)
            slider_combinations = []
            rng = max_value - min_value
            for i in range(0, rng, 2):
                if i == rng - 1:
                    break

                start = i
                end = i + 2
                slider_combinations.append((start, end))

            return slider_combinations

features_combinations = {
    'track_popularity': get_values('track_popularity'),
    'track_album_release_date': get_values('track_album_release_date'),
    'playlist_subgenre': get_values('playlist_subgenre'),
    'duration_in_minutes': get_values('duration_in_minutes'),
    'playlist_genre': get_values('playlist_genre'),
    'loudness': get_values('loudness'),
    'track_name': get_values('track_name'),
    'track_artist': get_values('track_artist'),
    'track_album_name': get_values('track_album_name')
}

with open('../data/features_combinations.json', "w", encoding='utf-8') as f:
    json.dump(features_combinations, f, indent=4)
