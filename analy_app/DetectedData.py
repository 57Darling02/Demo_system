import time
import streamlit as st
import Dynamic_render
from ResourcePool import resource_pool


@st.cache_data
def get_data(MaxDataId):
    df_detected_data = resource_pool.get_detected_data()
    while df_detected_data.empty:
        time.sleep(1)
        df_detected_data = resource_pool.get_detected_data()
    return df_detected_data
data = get_data(resource_pool.MaxDataId)
renderer = Dynamic_render.get_pyg_renderer(data)
tab1, tab2= st.tabs(
    ["静态数据表", "静态数据分析工具"]
)


with tab2:
    renderer.explorer(default_tab="vis")

with tab1:
    renderer.table()



