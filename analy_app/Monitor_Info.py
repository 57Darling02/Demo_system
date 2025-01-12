
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo, event
import streamlit as st
from ResourcePool import resource_pool
import Api as api
import html
from Dynamic_render import get_monitor_info, update_interval ,get_monitor_alive
import time
from st_aggrid import AgGrid, GridOptionsBuilder
@st.fragment
def render_monitor_list():
    st.session_state.timestamp = resource_pool.get_update_timestamp()
    st.session_state.df_monitor_info = get_monitor_info(st.session_state.timestamp)

    while st.session_state.df_monitor_info.empty:
        time.sleep(0.5)
        st.session_state.df_monitor_info = get_monitor_info(st.session_state.timestamp)
    st.markdown("### Monitor List")
    gb = GridOptionsBuilder.from_dataframe(st.session_state.df_monitor_info)
    go = gb.build()
    AgGrid(
        st.session_state.df_monitor_info,
        gridOptions=go,
        height=450,
        fit_columns_on_grid_load=True)

# @st.fragment(run_every=f"{update_interval}s")
@st.fragment
def render_monitor_chart():
    update_timestamp = resource_pool.get_update_timestamp()
    alive_monitor_number, all_monitor_number = get_monitor_alive(update_timestamp)
    def update():
        st.session_state.alive_monitor_number, st.session_state.all_monitor_number = get_monitor_alive(update_timestamp)

    st.markdown(f"### Monitor")
    st.markdown(f"#### Total : {all_monitor_number} alive : {alive_monitor_number}")
    with elements("Monitor"):
        event.Interval(update_interval, update)
        da = [
            {
                "id": "current",
                "data": [
                    {
                        "x": "online_monitor",
                        "y": alive_monitor_number
                    },
                    {
                        "x": "offline_monitor",
                        "y": all_monitor_number - alive_monitor_number
                    }
                ]
            },
            {
                "id": "total",
                "data": [
                    {
                        "x": "Total_monitor",
                        "y": all_monitor_number
                    }
                ]
            }
        ]
        with mui.Box(sx={"height": 500}):
            nivo.RadialBar(
                data=da,
                valueFormat=">-.2f",
                padding=0.4,
                cornerRadius=2,
                margin={"top": 20, "right": 140, "bottom": 20, "left": 20},
                radialAxisStart={"tickSize": 5, "tickPadding": 5, "tickRotation": 0},
                circularAxisOuter={"tickSize": 5, "tickPadding": 12, "tickRotation": 0},
                legends=[
                    {
                        "anchor": "right",
                        "direction": "column",
                        "justify": False,
                        "translateX": 80,
                        "translateY": 0,
                        "itemsSpacing": 6,
                        "itemDirection": "left-to-right",
                        "itemWidth": 100,
                        "itemHeight": 18,
                        "itemTextColor": "#999",
                        "symbolSize": 18,
                        "symbolShape": "square",
                        "effects": [
                            {
                                "on": "hover",
                                "style": {
                                    "itemTextColor": "#000"
                                }
                            }
                        ]
                    }
                ]
            )


c1,c2,c3 = st.columns([3,2,2])

with c3:
    st.markdown(f"## Register Monitor")
    with st.form("monitor_register_form"):
        st.number_input("monitor_id", key="monitor_id_box" ,step=1)
        st.text_input("Password", type="password", key="passwordbox")
        # 提交按钮
        submit_button = st.form_submit_button("register")
        if submit_button:
            info = st.info("Waiting...")
            # 获取表单输入的值
            monitor_id = st.session_state.monitor_id_box
            password = st.session_state.passwordbox
            resp = api.monitor_register(monitor_id, password,st.session_state.Token)
            info.empty()
            if resp is None:
                st.error("无法连接. 可能没开服务器？")
            elif resp["code"] != 200:
                st.error("**Error:** " + html.escape(resp["message"]))
                st.code(resp["data"])
            else:
                resource_pool.update_resource_pool()
                st.success("successful!")





with c2:
    # Dynamic_render.render_monitor_list()
    render_monitor_list()

with c1:
    render_monitor_chart()



