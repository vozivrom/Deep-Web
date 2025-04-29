from typing import Any

from features.feature import Feature


class TrackAlbumReleaseDate(Feature):
    def show_feature(self) -> Any:
        self.st.markdown('<div class="param_header">Track release date</div>', unsafe_allow_html=True)
        col1, col2 = self.st.columns(2)

        min_date = self.feature_info['min']
        max_date = self.feature_info['max']
        with col1:
            from_date = self.st.date_input(label='From date', min_value=min_date, max_value=max_date, value=min_date)

        with col2:
            to_date = self.st.date_input(label='To date', min_value=from_date, max_value=max_date, value=max_date)

        return str(from_date), str(to_date)
    