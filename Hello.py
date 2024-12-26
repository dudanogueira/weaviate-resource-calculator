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

import math

millnames = ['',' Thousand',' Million',' Billion',' Trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

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
      min_value=1, max_value=10000, value=384, step=1
    )
    calculate_submit = st.form_submit_button("calculate", use_container_width=True)

  if calculate_submit:
    object_number = 1e6
    each_vector = dimensions * 4
    bytes_per1mm = 2 * object_number * each_vector
    real_gb_per1mm = (object_number * each_vector)/1073741824
    gb_per1mm = bytes_per1mm / 1073741824
    max_connections = 32
    max_connections_memory_per_object = object_number * (max_connections * 10)
    gb_max_connections_memory = max_connections_memory_per_object/1073741824
    # 1e6 * (1536B + (64 * 10))
    max_connection_calculation = object_number * (each_vector + (max_connections * 10))
    st.markdown(f"Suggested [resource plan](https://weaviate.io/developers/weaviate/concepts/resources)")
    st.title(f"{gb_per1mm:.2f} GB memory")
    st.subheader(f"for {millify(object_number)} objects with {dimensions} dimensions")
    #st.subheader("Calculation")
    st.markdown(f"each vector with their {dimensions} dimensions will take **{each_vector/1000:.2f} Kilobytes**. For {object_number:.0f} objects, it amounts to **{real_gb_per1mm:.2f}** GB")
    st.markdown(f"As a rule of thumb, we double that to **{gb_per1mm:.2f}** GB")
    st.title(f"A more accurate memory calculation")
    st.markdown(f'''Let's calcualte the `maxConnections` instead of doubling the base requirement by 2.
By default, each object will have {max_connections} [maxConnections](https://weaviate.io/developers/weaviate/config-refs/schema/vector-index#hnsw-index-parameters)
each connection will take from 8-10B. So, for {object_number:.0f} objects, it amounts to **{max_connections_memory_per_object/1073741824:.2f}** GB''')
    st.markdown(f"{real_gb_per1mm:.2f}GB + {gb_max_connections_memory:.2f} GB = **{max_connection_calculation/1073741824:.2f} Gb**")
    st.title("What about CPU?")
    st.markdown("Read more about CPU here [here](https://weaviate.io/developers/weaviate/concepts/resources#the-role-of-cpus)")

if __name__ == "__main__":
  run()
