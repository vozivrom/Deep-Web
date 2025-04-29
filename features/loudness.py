from typing import Any

from features.feature import Feature


class Loudness(Feature):
    def show_feature(self) -> Any:
        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)

        options = ['Quiet', 'Normal', 'Loud']
        choice = self.st.pills(self.feature_name, options, selection_mode="single", label_visibility='collapsed')

        return choice
