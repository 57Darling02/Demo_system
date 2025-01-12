import streamlit as st
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo, event
from ResourcePool import resource_pool
from Dynamic_render import get_realtime_data, split_dataframe_by_column, process_for_linechart, get_detected_data
update_interval = resource_pool.update_interval
from predict_gex import predict

def process_data(split_dfs, monitor_id,column_y):
    result = []
    dfs = split_dfs.get(monitor_id)
    sorted_df = dfs.sort_values(by="collect_time")
    last_ten_records = sorted_df.tail(5)
    data_list = []
    for index, row in last_ten_records.iterrows():
        data_dict = {
            "x": str(row["collect_time"]).split('+')[0].split(' ')[1],
            "y": row[column_y]
        }
        data_list.append(data_dict)
    data_dict = {
        "id": monitor_id,
        "color": "hsl(150, 70%, 50%)",
        "data": data_list
    }
    result.append(data_dict)
    predict_data = predict(monitor_id=monitor_id, p_type=column_y)
    data_list = []
    for i in range(len(predict_data)):
        data_dict = {
            "x": f"Time+{i+1}",
            "y": predict_data[i]
        }
        data_list.append(data_dict)
    data_dict = {
        "id": f"predict {monitor_id}'s {column_y}",
        "color": "hsl(150, 70%, 50%)",
        "data": data_list
    }
    result.append(data_dict)
    return result
def update():
    st.session_state.realtime_data = get_realtime_data(resource_pool.update_timestamp)
    st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp),
                                                           'monitor_id')
# @st.fragment(run_every=f"10s")
@st.fragment
def render_predict():
    st.session_state.realtime_data = get_realtime_data(resource_pool.update_timestamp)
    st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp), 'monitor_id')

    layout = [
        # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
        dashboard.Item("choose_box", 9, 0, 3, 5),
        dashboard.Item("going_predict", 0, 0, 9, 5)
    ]
    with elements("dashboard"):
        event.Interval(update_interval, update)
        with dashboard.Grid(layout, draggableHandle=".draggable"):
            with mui.Card(key="choose_box", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="走势选择", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    monitor_ids = [item["monitor_id"] for item in st.session_state.realtime_data]
                    choose_columns = ["air_temperature",  "wind_speed"]
                    if not 'select_box1' in st.session_state or not 'select_box3' in st.session_state:
                        st.session_state.event = 1
                        st.session_state.select_box1 = monitor_ids[0]
                        st.session_state.select_box3 = choose_columns[0]
                    with mui.Box(sx={'width': '100%', 'height': '50%'}):  #
                        with mui.FormControl(fullWidth=True):  # FormControl 表单控制接口；fullWidth=True 全宽
                            mui.InputLabel('采集端id',
                                           id="monitor_id-select-label")  # InputLabel：输入标签，id 被 Select 引用👇

                            def on_Selectbox1(event, child):
                                print(event, child.props.value)
                                st.session_state.event = event
                                st.session_state.select_box1 = child.props.value

                            with mui.Select(
                                    autoWidth=False,  # 弹出窗口的宽度将根据菜单中的项目自动设置
                                    defaultOpen=False,  # 选择器选项是否默认打开
                                    # defaultValue='',  # 默认输入值；在组件不受客户端控制时使用
                                    # id='select',  # select 元素的id
                                    label="采集端id",  # 当InputLabel被引用时，充当占位符
                                    labelId="monitor_id-select-label",  # 引用 InputLabel 的标签id
                                    multiple=False,  # 菜单支持多项选择
                                    native=False,  # 原生select元素，一般不使用 False
                                    onChange=on_Selectbox1,  # 选择之后的回调
                                    # onClose=None,  # 当组件请求关闭时触发的回调
                                    # onOpen=None,  # 请求打开组件时触发的回调
                                    value=st.session_state.select_box1,  # 如果设置了value，那么value应该是MenuItem的value值
                                    variant='outlined',  # 变体
                            ):
                                for item in monitor_ids:
                                    mui.MenuItem(children=item, value=item)

                    with mui.Box(sx={'width': '100%', 'height': '50%'}):  #
                        with mui.FormControl(fullWidth=True):  # FormControl 表单控制接口；fullWidth=True 全宽
                            mui.InputLabel('查看项目', id="obj-select-label")  # InputLabel：输入标签，id 被 Select 引用👇
                            def on_Selectbox2(event, child):
                                print(event, child.props.value)
                                st.session_state.event = event
                                st.session_state.select_box3 = child.props.value

                            with mui.Select(
                                    autoWidth=False,  # 弹出窗口的宽度将根据菜单中的项目自动设置
                                    defaultOpen=False,  # 选择器选项是否默认打开
                                    # defaultValue='',  # 默认输入值；在组件不受客户端控制时使用
                                    # id='select',  # select 元素的id
                                    label="查看项目",  # 当InputLabel被引用时，充当占位符
                                    labelId="obj-select-label",  # 引用 InputLabel 的标签id
                                    multiple=False,  # 菜单支持多项选择
                                    native=False,  # 原生select元素，一般不使用 False
                                    onChange=on_Selectbox2,  # 选择之后的回调
                                    # onClose=None,  # 当组件请求关闭时触发的回调
                                    # onOpen=None,  # 请求打开组件时触发的回调
                                    value=st.session_state.select_box3,  # 如果设置了value，那么value应该是MenuItem的value值
                                    variant='outlined',  # 变体
                            ):
                                for item in choose_columns:
                                    mui.MenuItem(children=item, value=item)


            with mui.Card(key="going_predict", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="走势", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    # st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp), 'monitor_id')
                    nivo.Line(
                        data=process_data(st.session_state.split_dfs, st.session_state.select_box1, st.session_state.select_box3),
                        margin={"top": 50, "right": 110, "bottom": 50, "left": 60},
                        xScale={"type": "point"},
                        yScale={
                            "type": "linear",
                            "min": "auto",
                            "max": "auto",
                            "stacked": False,
                            "reverse": False
                        },
                        curve="cardinal",
                        axisTop=None,
                        axisRight=None,
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": f"monitor_id: {st.session_state.select_box1}",
                            "legendOffset": 36,
                            "legendPosition": "middle",
                            "truncateTickAt": 0
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": f"{st.session_state.select_box3}",
                            "legendOffset": -40,
                            "legendPosition": "middle",
                            "truncateTickAt": 0
                        },
                        pointSize=10,
                        pointColor={"theme": "background"},
                        pointBorderWidth=2,
                        pointBorderColor={"from": "serieColor"},
                        pointLabel="data.yFormatted",
                        pointLabelYOffset=-12,
                        enableTouchCrosshair=True,
                        useMesh=True,
                        legends=[
                            {
                                "anchor": "bottom-right",
                                "direction": "column",
                                "justify": False,
                                "translateX": 100,
                                "translateY": 0,
                                "itemsSpacing": 0,
                                "itemDirection": "left-to-right",
                                "itemWidth": 80,
                                "itemHeight": 20,
                                "itemOpacity": 0.75,
                                "symbolSize": 12,
                                "symbolShape": "circle",
                                "symbolBorderColor": "rgba(0, 0, 0,.5)",
                                "effects": [
                                    {
                                        "on": "hover",
                                        "style": {
                                            "itemBackground": "rgba(0, 0, 0,.03)",
                                            "itemOpacity": 1
                                        }
                                    }
                                ]
                            }
                        ]
                    )

render_predict()
