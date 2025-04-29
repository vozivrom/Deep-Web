import pandas as pd
import requests
import streamlit as st

from app.json_handler import JsonHandler
from features.loudness import Loudness
from features.playlist_genre import PlaylistGenre
from features.slider_feature import SliderFeature
from features.string_feature import StringFeature
from features.track_album_release_date import TrackAlbumReleaseDate

st.set_page_config(layout="wide")
header = st.markdown("<h1 style='text-align:center;'>Deep Web</h1>", unsafe_allow_html=True)

if 'k_max' not in st.session_state:
    st.session_state.k_max = 2

if 'show_df' not in st.session_state:
    st.session_state.show_df = False

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

features_params = JsonHandler.load_features_params('data/')

features_names = [feature_name for feature_name in list(features_params.keys()) for _ in range(2)]
features_names_iter = iter(features_names)

features = {next(features_names_iter): TrackAlbumReleaseDate(st, next(features_names_iter)),
            next(features_names_iter): PlaylistGenre(st, next(features_names_iter)),
            next(features_names_iter): PlaylistGenre(st, next(features_names_iter)),
            next(features_names_iter): SliderFeature(st, next(features_names_iter)),
            next(features_names_iter): SliderFeature(st, next(features_names_iter)),
            next(features_names_iter): Loudness(st, next(features_names_iter)),
            next(features_names_iter): StringFeature(st, next(features_names_iter)),
            next(features_names_iter): StringFeature(st, next(features_names_iter)),
            next(features_names_iter): StringFeature(st, next(features_names_iter))}

k_max_columns = st.columns([1,1,0.25], vertical_alignment='center')
with k_max_columns[0]:
    st.session_state.k_max = st.slider('Kmax', step=1, min_value=2, max_value=23450, value=50)
with k_max_columns[1]:
    st.session_state.k_max = st.number_input('Kmax', step=1, min_value=2, max_value=23450, value=50)
with k_max_columns[2]:
    if st.button('Submit', type='primary'):
        filtered_data = pd.DataFrame(requests.get("http://127.0.0.1:8000/filtered_data").json())
        k = filtered_data.shape[0]
        st.write(f'k = {k}')
        if k < st.session_state.k_max:
            st.session_state.show_df = True
        else:
            st.session_state.show_df = False
    if st.button('Reset'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

for i, feature in enumerate(features.values()):
    features_params[feature.feature_name] = feature.show_feature()

requests.put(f"http://127.0.0.1:8000/features_params", json=features_params)

if st.session_state.show_df:
    filtered_data = pd.DataFrame(requests.get("http://127.0.0.1:8000/filtered_data").json())
    st.write(filtered_data)
