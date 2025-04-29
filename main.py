import json
import os
import subprocess
import threading
import time

import pandas as pd
import requests
import uvicorn

from app.dataframe_handler import DFHandler
from app.json_handler import JsonHandler

features_combinations = JsonHandler.load_data("data/features_combinations.json")

k_max = 1000
df_len = DFHandler.get_original_df().shape[0]
features_params = {
    'track_popularity': None,
    'track_album_release_date': None,
    'playlist_subgenre': None,
    'playlist_genre': None,
    'duration_in_minutes': None,
    'loudness': None,
    'track_artist': None,
    'track_name': None,
    'track_album_name': None,
}

rebuilt_df = pd.DataFrame()
def main():
    global rebuilt_df
    filtered_df = pd.DataFrame()

    start_time = time.time()
    walk_tree(list(features_params.keys()), 25000, filtered_df)
    rebuilt_df.drop_duplicates(ignore_index=True, inplace=True)
    end_time = time.time()

    print(f"Dataset was built in : {end_time - start_time} seconds")

    rebuilt_df.to_csv('rebuilt_db.csv', index=False, sep=',')

def walk_tree(remaining_features: list[str], k: int, filtered_df):
    global rebuilt_df

    if rebuilt_df.shape[0] == df_len:
        print("Already rebuilt")
        return
    if not remaining_features:
        return

    current_feature = remaining_features[0]

    if k == 0: # no points in moving deeper
        features_params[current_feature] = None
        return
    elif k < k_max: # we can now save the data

        features_params[current_feature] = None

        fetched_df = pd.DataFrame(filtered_df)
        rebuilt_df = pd.concat([rebuilt_df, fetched_df], ignore_index=True)
        rebuilt_df.drop_duplicates(ignore_index=True, inplace=True)

        print(f'Current length of rebuilt database: {rebuilt_df.shape[0]}')
        return
    else: # k >= k_max
        if not remaining_features:
            print(f"Too many results at the leaf — unresolved")
            return

        for value in features_combinations[current_feature]:
            if isinstance(value, tuple):
                val = (value[0], value[1])
            else:
                if current_feature == 'playlist_genre' or current_feature == 'playlist_subgenre':
                    val = [value]
                else:
                    val = value

            features_params[current_feature] = val

            JsonHandler.save_features_params('data/', features_params)


            requests.put(
                f"http://127.0.0.1:8000/features_params",
                headers={"Content-Type": "application/json"},
                json=features_params
            )
            filtered_data = requests.get("http://127.0.0.1:8000/filtered_data").json()

            k = len(filtered_data)
            # if k < k_max:
            #     print(f"feature now is {current_feature}")
            walk_tree(remaining_features[1:], k, filtered_data)

        features_params[current_feature] = None

def run_fastapi():
    host = "0.0.0.0" if os.getenv("DOCKER_ENV") else "127.0.0.1"
    uvicorn.run("fastapi_app:app", host=host, port=8000, access_log=False)

def run_streamlit():
    subprocess.run(["streamlit", "run", "streamlit_app.py"], check=True)


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    time.sleep(2)

    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()

    time.sleep(2)

    # main()

    fastapi_thread.join()
    streamlit_thread.join()
