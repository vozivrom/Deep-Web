from typing import Any

from features.feature import Feature


class SliderFeature(Feature):
    def show_feature(self) -> Any:
        # Track Popularity and Duration in minutes

        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)

        start, end = self.st.slider(
            label=self.feature_name,
            min_value=0,
            max_value=self.feature_info['max'],
            value=(0, self.feature_info['max']),
            step=1,
            label_visibility='collapsed'
        )

        return start, end
