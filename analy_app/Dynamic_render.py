from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo, event
import streamlit as st
from ResourcePool import resource_pool
import time
from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import datetime
import functools
update_interval = resource_pool.update_interval

# @st.cache_resource
@functools.cache
def get_monitor_info(timestamp):
    df = resource_pool.get_monitor_info()
    return df

# @st.cache_data
@functools.cache
def get_monitor_alive(timestamp):
    df = get_monitor_info(timestamp)
    alive_time_strs = df['alive_time']
    alive_times = pd.to_datetime(alive_time_strs, format='%Y-%m-%d %H:%M:%S', errors='coerce')
    current_time = datetime.datetime.now()
    time_diffs = (current_time - alive_times).dt.total_seconds()
    alive_monitor_number = int((time_diffs < 8).sum())
    all_monitor_number = len(df)
    return alive_monitor_number, all_monitor_number
# @st.cache_data
# @st.fragment
@functools.cache
def get_realtime_data(timestamp):
    data = resource_pool.get_realtime_data()
    df = data
    df['rainfallColor'] = "hsl(8, 70%, 50%)"
    df['air_temperatureColor'] = "hsl(270, 70%, 50%)"
    df['humidityColor'] = "hsl(103, 70%, 50%)"
    df['wind_speedColor'] = "hsl(103, 70%, 50%)"
    df['air_pressureColor'] = "hsl(103, 70%, 50%)"

    # 选择需要的列并转换为所需格式
    result = df[['monitor_id', 'rainfall', 'rainfallColor', 'air_temperature', 'air_temperatureColor', 'humidity',
                 'humidityColor', 'wind_speed', "wind_speedColor", 'air_pressure', 'air_pressureColor']].to_dict(
        orient='records')
    return result

# @st.cache_data
@functools.cache
def get_detected_data(timestamp):
    df = resource_pool.get_detected_data()
    return df


# @st.cache_data
def split_dataframe_by_column(df, column_name):
    split_dfs = {value: group for value, group in df.groupby(column_name)}
    return split_dfs

# @st.cache_data
def process_for_linechart(split_dfs, monitor_id,column_y):
    result = []
    dfs = split_dfs.get(monitor_id)
    sorted_df = dfs.sort_values(by="collect_time")
    last_ten_records = sorted_df.tail(5)
    data_list = []
    for index, row in last_ten_records.iterrows():
        data_dict = {
            "x": str(row["collect_time"]).split('+')[0],
            "y": row[column_y]
        }
        data_list.append(data_dict)
    data_dict = {
        "id": monitor_id,
        "color": "hsl(150, 70%, 50%)",
        "data": data_list
    }
    result.append(data_dict)
    # print(f"result:{result}")
    return result




# @st.fragment(run_every=f"{update_interval}s")
# def render_monitor_chart():
#     update_timestamp = resource_pool.get_update_timestamp()
#     # print("render_monitor_chart")
#     alive_monitor_number, all_monitor_number = get_monitor_alive(update_timestamp)
#     def update():
#         st.session_state.alive_monitor_number, st.session_state.all_monitor_number = get_monitor_alive(update_timestamp)
#
#     st.markdown(f"### Monitor")
#     st.markdown(f"#### Total : {all_monitor_number} alive : {alive_monitor_number}")
#     with elements("Monitor"):
#         event.Interval(update_interval, update)
#         da = [
#             {
#                 "id": "current",
#                 "data": [
#                     {
#                         "x": "online_monitor",
#                         "y": alive_monitor_number
#                     },
#                     {
#                         "x": "offline_monitor",
#                         "y": all_monitor_number - alive_monitor_number
#                     }
#                 ]
#             },
#             {
#                 "id": "total",
#                 "data": [
#                     {
#                         "x": "Total_monitor",
#                         "y": all_monitor_number
#                     }
#                 ]
#             }
#         ]
#         with mui.Box(sx={"height": 500}):
#             nivo.RadialBar(
#                 data=da,
#                 valueFormat=">-.2f",
#                 padding=0.4,
#                 cornerRadius=2,
#                 margin={"top": 20, "right": 140, "bottom": 20, "left": 20},
#                 radialAxisStart={"tickSize": 5, "tickPadding": 5, "tickRotation": 0},
#                 circularAxisOuter={"tickSize": 5, "tickPadding": 12, "tickRotation": 0},
#                 legends=[
#                     {
#                         "anchor": "right",
#                         "direction": "column",
#                         "justify": False,
#                         "translateX": 80,
#                         "translateY": 0,
#                         "itemsSpacing": 6,
#                         "itemDirection": "left-to-right",
#                         "itemWidth": 100,
#                         "itemHeight": 18,
#                         "itemTextColor": "#999",
#                         "symbolSize": 18,
#                         "symbolShape": "square",
#                         "effects": [
#                             {
#                                 "on": "hover",
#                                 "style": {
#                                     "itemTextColor": "#000"
#                                 }
#                             }
#                         ]
#                     }
#                 ]
#             )
#

# @st.fragment
# def render_monitor_list():
#     st.session_state.timestamp = resource_pool.get_update_timestamp()
#     st.session_state.df_monitor_info = get_monitor_info(st.session_state.timestamp)
#     def update():
#         st.session_state.timestamp = resource_pool.get_update_timestamp()
#         st.session_state.df_monitor_info = get_monitor_info(st.session_state.timestamp)
#     while st.session_state.df_monitor_info.empty:
#         time.sleep(0.5)
#         st.session_state.df_monitor_info = get_monitor_info(st.session_state.timestamp)
#     st.markdown("### Monitor List")
#     gb = GridOptionsBuilder.from_dataframe(st.session_state.df_monitor_info)
#     go = gb.build()
#     AgGrid(
#         st.session_state.df_monitor_info,
#         gridOptions=go,
#         height=450,
#         fit_columns_on_grid_load=True)

from pygwalker.api.streamlit import StreamlitRenderer
@st.cache_resource
def get_pyg_renderer(df) -> "StreamlitRenderer":
    return StreamlitRenderer(df, kernel_computation=True, default_tab="data", spec="./config.json")