import pandas as pd

df = pd.read_csv('spotify_songs.csv')

# df.drop(['track_id', 'track_album_id'], axis=1, inplace=True)
# df.dropna(subset=['track_name', 'track_artist', 'track_album_name'], inplace=True)
# df = df.reset_index(drop=True)
#
# def convert_date(val):
#     if len(val.split('-')) == 1:  # Only year
#         return pd.to_datetime(val + '-01-01', format='%Y-%m-%d')
#     elif len(val.split('-')) == 2:
#         return pd.to_datetime(val + '-01', format='%Y-%m-%d')
#     else:
#         return pd.to_datetime(val, format='%Y-%m-%d')
#
# df['track_album_release_date'] = df['track_album_release_date'].apply(convert_date)
df['track_album_release_date'] = pd.to_datetime(df['track_album_release_date'])

# df.drop('playlist_id', axis=1, inplace=True)
# df.to_csv('spotify_songs.csv', index=False)

print(df.info())
