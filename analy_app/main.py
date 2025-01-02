import html

import streamlit as st
import Api as api

def login_page():
    st.session_state.current_page = 'login_page'
    st.title("Login Page")
    # 使用 columns 来实现居中布局，由于我们只需要一个元素，所以创建一个包含一个元素的列
    col = st.columns(1)[0]
    with col:
        # 创建一个表单
        with st.form("login_form"):
            st.text_input("Username", key="usernamebox")
            st.text_input("Password", type="password", key="passwordbox")
            # 提交按钮
            submit_button = st.form_submit_button("Submit")
            if submit_button:
                # 获取表单输入的值
                username = st.session_state.usernamebox
                password = st.session_state.passwordbox
                resp = api.login(username, password)

                if resp is None:
                    st.error("无法连接. 可能没开服务器？")
                elif resp["code"] != 200:
                    st.error("**Error:** "+ html.escape(resp["message"]) )
                    st.code(resp["data"])
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.password = password
                    st.session_state.token = resp["data"]
                    st.success("Login successful!")
                    home_page()
                    st.rerun()


def home_page():
    st.session_state.current_page = 'home_page'
    st.title("Home Page")
    st.write("Welcome to the home page!")
    # 使用 st.radio 进行页面选择



page_functions = {
        'login_page': login_page,
        'home_page': home_page,
    }
def main():

    # 检测状态完整性
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'login_page'

    #检测登入状态
    if not st.session_state.logged_in:
        login_page()
    else:
        try:
            page_functions[st.session_state.current_page]()
        except KeyError:
            st.error("Invalid page. Please try again.")





if __name__ == "__main__":
    main()