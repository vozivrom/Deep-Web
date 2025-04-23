import pandas as pd
from pandas import DataFrame
import streamlit as st
import numpy as np
import requests

from features import *

df = pd.read_csv('spotify_songs.csv')
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

st.set_page_config(layout="wide")
header = st.markdown("<h1 style='text-align:center;'>Deep Web</h1>", unsafe_allow_html=True)

if 'counter' not in st.session_state:
    st.session_state.counter = 0

# st.write(st.session_state.counter)


if "start" not in st.session_state:
    st.session_state.start = False

if 'k' not in st.session_state:
    # st.session_state.k = df.shape[0]
    st.session_state.k = np.full(9, df.shape[0])
    st.session_state.k_max = 2

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

st.session_state.filtered_df = df
df_adapter = DFAdapter(st.session_state.filtered_df)

default_feature_params = {'st': st, 'df_adapter': df_adapter}

features = {'track_album_release_date': TrackAlbumReleaseDate(**{**default_feature_params, 'feature_name': 'track_album_release_date'}),
            'playlist_genre': PlaylistGenre(**{**default_feature_params, 'feature_name': 'playlist_genre'}),
            'playlist_subgenre': Feature(**{**default_feature_params, 'feature_name': 'playlist_subgenre'}),
            'track_popularity': SliderFeature(**{**default_feature_params, 'feature_name': 'track_popularity'}),
            'duration_in_minutes': SliderFeature(**{**default_feature_params, 'feature_name': 'duration_in_minutes'}),
            'loudness': Loudness(**{**default_feature_params, 'feature_name': 'loudness'}),
            'track_artist': StringFeature(**{**default_feature_params, 'feature_name': 'track_artist'}),
            'track_album_name': StringFeature(**{**default_feature_params, 'feature_name': 'track_album_name'}),
            'track_name': StringFeature(**{**default_feature_params, 'feature_name': 'track_name'})}

k_max_columns = st.columns([1,1,0.25])
with k_max_columns[0]:
    st.session_state.k_max = st.slider('Kmax', disabled=st.session_state.start, step=1, min_value=2, max_value=len(df), value=2)
with k_max_columns[1]:
    st.session_state.k_max = st.number_input('Kmax', step=1, disabled=st.session_state.start, min_value=2, max_value=len(df), value=st.session_state.k_max)
with k_max_columns[2]:
    if st.button('Start', type='primary'):
        st.session_state.start = True

    if st.button('Reset'):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

st.header('Choose features to use:')
features_columns = st.columns(3)

for i, feature in enumerate(df.columns):
    with features_columns[i // 3]:
        label = str(feature.replace('_', ' ')).capitalize()
        checkbox = None

        if feature == 'playlist_subgenre':
            checkbox = st.checkbox(label=label, value=features[feature].enabled, disabled=st.session_state.start, on_change=lambda: st.session_state.update({'playlist_genre': True}) if st.session_state.playlist_subgenre else None, key=feature)
        elif feature == 'playlist_genre':
            checkbox = st.checkbox(label=label, value=features[feature].enabled, disabled=st.session_state.start, on_change=lambda: st.session_state.update({'playlist_subgenre': False}) if not st.session_state.playlist_genre else None, key=feature)
        else:
            checkbox = st.checkbox(label=label, value=features[feature].enabled, disabled=st.session_state.start, key=feature)

        if checkbox:
            features[feature].enabled = True
            # st.session_state.k[i] = df.shape[0]

if st.session_state.start:
    for i, feature in enumerate(features.values()):
        if feature.enabled and feature.feature_name != 'playlist_subgenre':
            # st.write(f'i = {i}')
            st.session_state.filtered_df, st.session_state.k[i] = feature.show_feature(st.session_state.filtered_df, st.session_state.k[i], st.session_state.k_max)
            if st.session_state.k[i] < st.session_state.k_max:
                st.session_state.k[i + 1:] = -1
            # st.write(st.session_state.k)

# st.write(f'k = {st.session_state.k}, k_max = {st.session_state.k_max}')
st.session_state.counter += 1
