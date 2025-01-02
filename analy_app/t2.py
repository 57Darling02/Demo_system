
import streamlit as st
from streamlit_elements import elements, mui
# st.set_page_config(layout='wide')

if not 'value' in st.session_state:
    st.session_state.event = 1
    st.session_state.value = ''
with elements(key='test1_Select'):  # 定义元素
    def on_Select(event, child):
        print(event, child.props.value)
        st.session_state.event = event
        st.session_state.value = child.props.value
    with mui.Box(sx={'width': '120px', 'height': '320px'}):  #
        with mui.FormControl(fullWidth=True):  # FormControl 表单控制接口；fullWidth=True 全宽
            mui.InputLabel('Age', id="demo-simple-select-label")  # InputLabel：输入标签，id 被 Select 引用👇
            with mui.Select(
                autoWidth=False,  # 弹出窗口的宽度将根据菜单中的项目自动设置
                defaultOpen=False,  # 选择器选项是否默认打开
                # defaultValue='',  # 默认输入值；在组件不受客户端控制时使用
                # id='select',  # select 元素的id
                label="Age",  # 当InputLabel被引用时，充当占位符
                # labelId="demo-simple-select-label",  # 引用 InputLabel 的标签id
                multiple=False,  # 菜单支持多项选择
                native=False,  # 原生select元素，一般不使用 False
                onChange=on_Select,  # 选择之后的回调
                # onClose=None,  # 当组件请求关闭时触发的回调
                # onOpen=None,  # 请求打开组件时触发的回调
                value=st.session_state.value,  # 如果设置了value，那么value应该是MenuItem的value值
                variant='outlined',  # 变体
            ):
                mui.MenuItem(children='空', value='')
                mui.MenuItem(children='one', value=10)  # MenuItem：菜单项，当native=False时使用
                mui.MenuItem('two', value=20)  #
                mui.MenuItem('three', value=30)
