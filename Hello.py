# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

LOGGER = get_logger(__name__)


def run():
  st.set_page_config(
      page_title="Weaviate Resource Calculator",
      page_icon="👋",
  )
  # 2 * 1e6 * (256 * 4)
  st.write("# Weaviate Resource Calculator 👋")
  with st.form("calculate", clear_on_submit=False):
    dimensions = st.number_input(
      "Dimensions", key="dimension", placeholder="The number of dimensions",
      min_value=1, max_value=10000
    )
    calculate_submit = st.form_submit_button("calculate", use_container_width=True)

  if calculate_submit:
    bytes_per1mm = 2 * 1000000 * (dimensions * 4)
    gb_per1mm = bytes_per1mm / 1073741824
    st.text(f"For 1 million objects with {dimensions} dimensions, you will need 2 * 1e6 * (256 * 4):")
    st.markdown(f"## {gb_per1mm:.2f} GB")

if __name__ == "__main__":
  run()
