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

class WeaviateResourceCalculator:
  def __init__(self, object_number=1000000, dimensions=384, max_connections=32):
    self.object_number = object_number
    self.dimensions = dimensions
    self.max_connections = max_connections
    self.each_vector = dimensions * 4
    self.each_object_connections = self.max_connections * 10
    # first calculation, doubling the base requirement
    self.real_memory_usage = object_number * self.each_vector
    self.total_memory_usage = 2 * self.real_memory_usage
    # second calculation, more accurate, using max connections
    # 1e6 * (1536B + (64 * 10))
    self.connections_memory_usage = self.object_number * self.each_object_connections
    self.real_and_connections_memory_usage = self.real_memory_usage + self.connections_memory_usage
    pass

def run():
  st.set_page_config(
      page_title="Weaviate Resource Calculator",
      #page_icon="https://weaviate.io/img/favicon.ico",
      page_icon="🔢"
  )
  # 2 * 1e6 * (256 * 4)
  st.write("# Weaviate Resource Calculator")
  with st.form("calculate", clear_on_submit=False):
    dimensions = st.number_input(
      "Dimensions", key="dimension", placeholder="The number of dimensions",
      min_value=1, max_value=10000, value=384, step=1
    )
    object_number = st.number_input(
      "Object Number", key="object_number", placeholder="How  many objects to store",
      min_value=10000, value=1000000, step=1
    )
    max_connections = st.number_input(
      "Max Connections", key="max_connections", placeholder="The number of connections per object",
      min_value=1, max_value=10000, value=32, step=1
    )
    calculate_submit = st.form_submit_button("calculate", use_container_width=True)

  if calculate_submit:
    calculation = WeaviateResourceCalculator(
      object_number=object_number,
      dimensions=dimensions,
      max_connections=max_connections
      )
    
    st.markdown(f"Suggested [resource plan](https://weaviate.io/developers/weaviate/concepts/resources). Learn more about Weaviate")
    st.title(f"{calculation.total_memory_usage/1073741824:.2f} GB memory")
    st.subheader(f"for {millify(calculation.object_number)} objects with {calculation.dimensions} dimensions")
    #st.subheader("Calculation")
    st.markdown(f"each vector with their {calculation.dimensions} dimensions will take **{calculation.each_vector/1000:.2f} Kilobytes**. For {calculation.object_number:.0f} objects, it amounts to **{calculation.real_memory_usage/1073741824:.2f}** GB")
    st.markdown(f"As a rule of thumb, we double that to **{calculation.total_memory_usage/1073741824:.2f}** GB")
    st.title(f"A more accurate memory calculation")
    st.markdown(f'''Let's calculate the `maxConnections` instead of doubling the base requirement.
By default, each object will have {calculation.max_connections} [maxConnections](https://weaviate.io/developers/weaviate/config-refs/schema/vector-index#hnsw-index-parameters).
Each connection will take from 8-10B, adding {calculation.each_object_connections/1000:.2f} Kilobytes per object. 

So, for {calculation.object_number:.0f} objects, it amounts to **{calculation.connections_memory_usage/1073741824:.2f}** GB''')
    st.markdown(f"{calculation.real_memory_usage/1073741824:.2f} GB (for the objects) + {calculation.connections_memory_usage/1073741824:.2f} GB (for the connections) = **{calculation.real_and_connections_memory_usage/1073741824:.2f} Gb**")
    st.title(f"What about CPU?")
    st.markdown("Read more about CPU here [here](https://weaviate.io/developers/weaviate/concepts/resources#the-role-of-cpus)")
  st.divider()
  title_container = st.container()
  col1, col2 = st.columns([1, 20])
  with title_container:
      with col1:
        st.image(
            "https://avatars.githubusercontent.com/u/37794290?s=48&v=4",
            width=48
        )
      with col2:
          st.markdown('Learn more about <a href="http://weaviate.io">Weaviate</a>',
                      unsafe_allow_html=True)      

if __name__ == "__main__":
  run()
