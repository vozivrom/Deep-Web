from typing import Any

from features.feature import Feature


class StringFeature(Feature):
    def show_feature(self) -> Any:
        feature_name = str(self.feature_name.replace('_', ' ')).capitalize()
        self.st.markdown(f'<div class="param_header">{feature_name}</div>', unsafe_allow_html=True)
        user_input = self.st.text_input(label=self.feature_name, key=self.feature_name, label_visibility='collapsed')

        return user_input
