import pandas as pd
from pandas import DataFrame
import streamlit as st
import numpy as np
import requests

from app.dataset_rebuild import features_params

from features.track_album_release_date import TrackAlbumReleaseDate
from features.playlist_genre import PlaylistGenre
from features.string_feature import StringFeature
from features.slider_feature import SliderFeature
from features.loudness import Loudness

df = pd.read_csv('data/spotify_songs.csv')
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

st.set_page_config(layout="wide")
header = st.markdown("<h1 style='text-align:center;'>Deep Web</h1>", unsafe_allow_html=True)

if 'k' not in st.session_state:
    st.session_state.k = np.full(8, df.shape[0])
    st.session_state.k_max = 2

if 'filtered_df' not in st.session_state:
    st.session_state.filtered_df = [df for _ in range(0, 8)]

st.markdown(
    """
    <style>
    .param_header {
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

features_names = [feature_name for feature_name in [
    'track_album_release_date', 'playlist_genre', 'track_popularity',
    'duration_in_minutes', 'loudness', 'track_artist',
    'track_album_name', 'track_name'
] for _ in range(3)]
features_names_iter = iter(features_names)

features = {next(features_names_iter): TrackAlbumReleaseDate(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): PlaylistGenre(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): SliderFeature(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): SliderFeature(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): Loudness(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): StringFeature(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): StringFeature(st, next(features_names_iter), features_params[next(features_names_iter)]),
            next(features_names_iter): StringFeature(st, next(features_names_iter), features_params[next(features_names_iter)])}

k_max_columns = st.columns([1,1,0.25], vertical_alignment='bottom')
with k_max_columns[0]:
    st.session_state.k_max = st.slider('Kmax', step=1, min_value=2, max_value=len(df), value=features_params['k_max'])
with k_max_columns[1]:
    st.session_state.k_max = st.number_input('Kmax', step=1, min_value=2, max_value=len(df), value=features_params['k_max'])
    # requests.put("http://127.0.0.1:8000/k_max", json={'name': 'k_max', 'value': st.session_state.k_max})
with k_max_columns[2]:
    if st.button('Reset'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

for feature in features.values():
    if st.button(f'Get {feature.feature_name}'):
        feature_json = requests.get(f"http://127.0.0.1:8000/{feature.feature_name}").json()
        st.write(feature_json)

for i, feature in enumerate(features.values()):
    st.session_state.filtered_df[i], st.session_state.k[i] = feature.show_feature(st.session_state.filtered_df[i - 1] if i > 0 else df,
                                                                                  st.session_state.k[i], st.session_state.k_max)
    # feature_json = requests.get(f"http://127.0.0.1:8000/{feature.feature_name}").json()
    # st.write(feature_json)
