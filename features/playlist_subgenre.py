from typing import Any

from feature import Feature


class PlaylistSubgenre(Feature):
    def show_feature(self) -> Any:
        self.st.markdown('<div class="param_header">Playlist subgenres</div>', unsafe_allow_html=True)

        sub_genres_choice = self.st.multiselect(
            label=self.feature_name,
            options=self.feature_info,
            label_visibility='collapsed'
        )

        return sub_genres_choice