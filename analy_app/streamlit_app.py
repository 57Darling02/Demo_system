import streamlit as st
import html
import Api as api
from st_pages import get_nav_from_toml
from ResourcePool import resource_pool
def login():
    # st.session_state.current_page = 'login_page'
    # 使用 columns 来实现居中布局，由于我们只需要一个元素，所以创建一个包含一个元素的列
    _,col,_ = st.columns([3,4,3])
    with col:
        # 创建一个表单
        with st.form("login_form"):
            st.text_input("Username", key="usernamebox")
            st.text_input("Password", type="password", key="passwordbox")
            # 提交按钮
            submit_button = st.form_submit_button("login")
            if submit_button:
                info = st.info("Logging in...")
                # 获取表单输入的值
                username = st.session_state.usernamebox
                password = st.session_state.passwordbox
                resp = api.login(username, password)
                info.empty()
                if resp is None:
                    st.error("无法连接. 可能没开服务器？")
                elif resp["code"] != 200:
                    st.error("**Error:** " + html.escape(resp["message"]))
                    st.code(resp["data"])
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.Token = resp["data"]
                    st.success("Login successful!")
                    st.rerun()
@st.dialog("Sure?")
def logout():
    st.write(f"Sure to logout ?")
    if st.button("Sure"):
        st.session_state.logged_in = False
        st.rerun()

try:
    st.set_page_config(layout="wide")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    login_page = st.Page(login, title="Log in", icon=":material/login:")
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    if st.session_state.logged_in:
        nav = get_nav_from_toml(".streamlit/pages.toml")
        nav["Log out"] = [logout_page]
        pg = st.navigation(nav)
    else:
        pg = st.navigation([login_page])
    # add_page_title(pg)
    pg.run()
except InterruptedError:
    print("Cleaning up...")
    resource_pool.scheduler.shutdown()
    st.stop()
