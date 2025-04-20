import pandas as pd
import streamlit as st

from csv_adapter import CSVAdapter

df = pd.read_csv('spotify_songs.csv')
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

st.set_page_config(layout="wide")
header = st.markdown("<h1 style='text-align:center;'>Deep Web</h1>", unsafe_allow_html=True)

k_max = st.slider('Kmax', step=1, max_value=len(df))
k_max = st.number_input('Kmax', step=1, max_value=len(df), value=k_max)


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

csv_adapter = CSVAdapter(df)

genres, date = st.columns([4,2], border=True)

with genres:
        st.markdown('<div class="param_header">Playlist genre</div>', unsafe_allow_html=True)

        genres_choice = st.multiselect(
            label='',
            options=csv_adapter.get_genres(),
            default=[]
        )

        if genres_choice:

            filtered_df = df[df['playlist_genre'].isin(genres_choice)]
            k = len(filtered_df)
            st.write(f'k = {k}')

            if k <= k_max:
                st.write(filtered_df)
            else:
                sub_genres = st.columns(len(genres_choice), border=True)
                for i, sub_genre in enumerate(sub_genres):
                    with sub_genre:
                        st.markdown('<div class="param_header">Playlist subgenre</div>', unsafe_allow_html=True)

                        sub_genres_choice = st.multiselect(
                            label='',
                            options=csv_adapter.get_subgenres(genres_choice[i]),
                            default=[]
                        )

                        if sub_genres_choice:
                            filtered_df = df[df['playlist_subgenre'].isin(sub_genres_choice)]
                            k = len(filtered_df)
                            st.write(f'k = {k}')
                            if k <= k_max:
                                st.write(filtered_df)


with date:
    st.markdown('<div class="param_header">Track release date</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        from_date = pd.to_datetime(st.date_input(label='From date', value=None))

    with col2:
        to_date = pd.to_datetime(st.date_input(label='To date', value=None))

    filtered_df = None
    if from_date and not to_date:
        filtered_df = df[df['track_album_release_date'] >= from_date]
    elif not from_date and to_date:
        filtered_df = df[df['track_album_release_date'] <= to_date]
    elif from_date and to_date:
        mask = (df['track_album_release_date'] >= from_date) & (df['track_album_release_date'] <= to_date)
        filtered_df = df[mask]

    if from_date or to_date:
        k = len(filtered_df)
        st.write(f'k = {k}')
        if k <= k_max:
            st.write(filtered_df)
