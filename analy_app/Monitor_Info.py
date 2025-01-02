

import streamlit as st
from ResourcePool import resource_pool
import Api as api
import html
import Dynamic_render

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
    Dynamic_render.render_monitor_list()

with c1:
    Dynamic_render.render_monitor_chart()



