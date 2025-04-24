from pandas import DataFrame

from features.feature import Feature
from app.dataframe_handler import DFHandler

class PlaylistGenre(Feature):
    def show_feature(self, df: DataFrame, k: int, k_max: int) -> (DataFrame, int):
        # GENRES

        self.st.markdown('<div class="param_header">Playlist genres</div>', unsafe_allow_html=True)
        genres_choice = self.st.multiselect(
            label='',
            options=list(df['playlist_genre'].unique()),
            default=[]
        )
        filtered_df = df
        if genres_choice:
            filtered_df = df[df['playlist_genre'].isin(genres_choice)]
            k = len(filtered_df)
            self.st.write(f'k = {k}')

            if k < k_max:
                self.st.write(filtered_df)

            # SUBGENRES
            self.st.markdown('<div class="param_header">Playlist subgenres</div>', unsafe_allow_html=True)
            subgenres = []

            for _ in genres_choice:
                subgenres += list(filtered_df['playlist_subgenre'].unique())

            sub_genres_choice = self.st.multiselect(
                label='',
                options=subgenres,
                default=[]
            )

            if sub_genres_choice:
                filtered_df = filtered_df[filtered_df['playlist_subgenre'].isin(sub_genres_choice)]
                k = len(filtered_df)
                self.st.write(f'k = {k}')
                if k < k_max:
                    self.st.write(filtered_df)

        df_handler = DFHandler(filtered_df)
        df_handler.put_df(self.feature_name)

        return filtered_df, len(filtered_df)
