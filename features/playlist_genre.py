from typing import Any

from features.feature import Feature


class PlaylistGenre(Feature):
    def show_feature(self) -> Any:
        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)

        genres_choice = self.st.multiselect(
            label=self.feature_name,
            options=self.feature_info,
            label_visibility = 'collapsed'
        )
        return genres_choice
