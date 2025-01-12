import streamlit as st
from streamlit_elements import elements, dashboard, mui, editor, media, lazy, sync, nivo, event
from ResourcePool import resource_pool
from Dynamic_render import get_monitor_alive, get_realtime_data, split_dataframe_by_column, process_for_linechart, get_detected_data
update_interval = resource_pool.update_interval
# @st.fragment(run_every=f"{update_interval}s")
#
# def update():
#     st.session_state.alive_monitor_number, st.session_state.all_monitor_number = get_monitor_alive(
#         resource_pool.update_timestamp)
#     st.session_state.realtime_data = get_realtime_data(resource_pool.update_timestamp)
#     st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp),
#                                                            'monitor_id')
@st.fragment(run_every=f"{update_interval}s")
def render_dashboard():
    st.session_state.alive_monitor_number, st.session_state.all_monitor_number = get_monitor_alive(resource_pool.update_timestamp)
    st.session_state.realtime_data = get_realtime_data(resource_pool.update_timestamp)
    st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp), 'monitor_id')

    layout = [
        # Chart item is positioned in coordinates x=6 and y=0, and takes 6/12 columns and has a height of 3.
        dashboard.Item("MonitorStatus", 0, 0, 3, 3),
        dashboard.Item("realtime_box", 3, 0, 6, 3),
        dashboard.Item("choose_box", 9, 0, 3, 5),
        dashboard.Item("going", 0, 4, 9, 2)
    ]
    with elements("dashboard"):
        # event.Interval(update_interval, update)
        with dashboard.Grid(layout, draggableHandle=".draggable"):

            with mui.Card(key="choose_box", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="走势选择", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    monitor_ids = [item["monitor_id"] for item in st.session_state.realtime_data]
                    choose_columns = ["rainfall", "air_temperature", "humidity", "wind_speed", "air_pressure","wind_direction"]
                    if not 'select_box1' in st.session_state or not 'select_box2' in st.session_state:
                        st.session_state.event = 1
                        st.session_state.select_box1 = monitor_ids[0]
                        st.session_state.select_box2 = choose_columns[0]

                    with mui.Box(sx={'width': '100%', 'height': '50%'}):  #
                        with mui.FormControl(fullWidth=True):  # FormControl 表单控制接口；fullWidth=True 全宽
                            mui.InputLabel('Monitor_id',
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
                                    label="Monitor_id",  # 当InputLabel被引用时，充当占位符
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
                            mui.InputLabel('obj', id="obj-select-label")  # InputLabel：输入标签，id 被 Select 引用👇
                            def on_Selectbox2(event, child):
                                print(event, child.props.value)
                                st.session_state.event = event
                                st.session_state.select_box2 = child.props.value

                            with mui.Select(
                                    autoWidth=False,  # 弹出窗口的宽度将根据菜单中的项目自动设置
                                    defaultOpen=False,  # 选择器选项是否默认打开
                                    # defaultValue='',  # 默认输入值；在组件不受客户端控制时使用
                                    # id='select',  # select 元素的id
                                    label="Object",  # 当InputLabel被引用时，充当占位符
                                    labelId="obj-select-label",  # 引用 InputLabel 的标签id
                                    multiple=False,  # 菜单支持多项选择
                                    native=False,  # 原生select元素，一般不使用 False
                                    onChange=on_Selectbox2,  # 选择之后的回调
                                    # onClose=None,  # 当组件请求关闭时触发的回调
                                    # onOpen=None,  # 请求打开组件时触发的回调
                                    value=st.session_state.select_box2,  # 如果设置了value，那么value应该是MenuItem的value值
                                    variant='outlined',  # 变体
                            ):
                                for item in choose_columns:
                                    mui.MenuItem(children=item, value=item)

            with mui.Card(key="MonitorStatus", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="Monitor status", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    alive_monitor_number, all_monitor_number = st.session_state.alive_monitor_number, st.session_state.all_monitor_number
                    da = [
                        {"id": "online_monitor", "label": "online_monitor", "value": alive_monitor_number,
                         "color": "hsl(120, 70%, 70%)"},
                        {"id": "offline_monitor", "label": "offline_monitor", "value": all_monitor_number - alive_monitor_number,
                         "color": "hsl(0, 0%, 30%)"}
                    ]
                    nivo.Pie(
                        data=da,
                        margin={"top": 10, "right": 10, "bottom": 80, "left": 10},
                        innerRadius=0.5,
                        padAngle=0.7,
                        cornerRadius=3,
                        activeOuterRadiusOffset=8,
                        borderWidth=1,
                        borderColor={
                            "from": "color",
                            "modifiers": [
                                ["darker", 0.2]
                            ]
                        },
                        arcLinkLabelsSkipAngle=10,
                        arcLinkLabelsTextColor="#333333",
                        arcLinkLabelsThickness=2,
                        arcLinkLabelsColor={"from": "color"},
                        arcLabelsSkipAngle=10,
                        arcLabelsTextColor={
                            "from": "color",
                            "modifiers": [
                                ["darker", 2]
                            ]
                        },
                        defs=[
                            {
                                "id": "dots",
                                "type": "patternDots",
                                "background": "inherit",
                                "color": "rgba(255, 255, 255, 0.3)",
                                "size": 4,
                                "padding": 1,
                                "stagger": True
                            },
                            {
                                "id": "lines",
                                "type": "patternLines",
                                "background": "inherit",
                                "color": "rgba(255, 255, 255, 0.3)",
                                "rotation": -45,
                                "lineWidth": 6,
                                "spacing": 10
                            }
                        ],

                        legends=[
                            {
                                "anchor": "bottom",
                                "direction": "row",
                                "justify": False,
                                "translateX": 0,
                                "translateY": 56,
                                "itemsSpacing": 0,
                                "itemWidth": 100,
                                "itemHeight": 18,
                                "itemTextColor": "#999",
                                "itemDirection": "left-to-right",
                                "itemOpacity": 1,
                                "symbolSize": 18,
                                "symbolShape": "circle",
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

            with mui.Card(key="realtime_box", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="realtime_box", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    nivo.Bar(
                        data= st.session_state.realtime_data,
                        # data=sync("realtime_data"),
                        keys=[
                            'rainfall',
                            'air_temperature',
                            'humidity',
                            'wind_speed',
                            'air_pressure'
                        ],
                        indexBy="monitor_id",
                        margin={"top": 50, "right": 130, "bottom": 50, "left": 60},
                        padding=0.3,
                        groupMode="grouped",
                        valueScale={"type": "linear"},
                        indexScale={"type": "band", "round": True},
                        colors={"scheme": "nivo"},
                        defs=[
                            {
                                "id": "dots",
                                "type": "patternDots",
                                "background": "inherit",
                                "color": "#38bcb2",
                                "size": 4,
                                "padding": 1,
                                "stagger": True
                            },
                            {
                                "id": "lines",
                                "type": "patternLines",
                                "background": "inherit",
                                "color": "#eed312",
                                "rotation": -45,
                                "lineWidth": 6,
                                "spacing": 10
                            }
                        ],
                        borderColor={
                            "from": "color",
                            "modifiers": [
                                ["darker", 1.6]
                            ]
                        },
                        axisTop=None,
                        axisRight=None,
                        axisBottom={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "monitor_id",
                            "legendPosition": "middle",
                            "legendOffset": 32,
                            "truncateTickAt": 0
                        },
                        axisLeft={
                            "tickSize": 5,
                            "tickPadding": 5,
                            "tickRotation": 0,
                            "legend": "realtime data",
                            "legendPosition": "middle",
                            "legendOffset": -40,
                            "truncateTickAt": 0
                        },
                        labelSkipWidth=12,
                        labelSkipHeight=12,
                        labelTextColor={
                            "from": "color",
                            "modifiers": [
                                ["darker", 1.6]
                            ]
                        },
                        legends=[
                            {
                                "dataFrom": "keys",
                                "anchor": "bottom-right",
                                "direction": "column",
                                "justify": False,
                                "translateX": 120,
                                "translateY": 0,
                                "itemsSpacing": 2,
                                "itemWidth": 100,
                                "itemHeight": 20,
                                "itemDirection": "left-to-right",
                                "itemOpacity": 0.85,
                                "symbolSize": 20,
                                "effects": [
                                    {
                                        "on": "hover",
                                        "style": {
                                            "itemOpacity": 1
                                        }
                                    }
                                ]
                            }
                        ],
                        role="application",
                        ariaLabel="Nivo bar chart demo",
                        barAriaLabel=lambda e: f"{e['id']}: {e['formattedValue']} in monitor: {e['indexValue']}"
                    )


            with mui.Card(key="going", sx={"display": "flex", "flexDirection": "column"}):
                mui.CardHeader(title="走势", className="draggable")
                with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                    # st.session_state.split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp), 'monitor_id')
                    nivo.Line(
                        data=process_for_linechart(st.session_state.split_dfs, st.session_state.select_box1, st.session_state.select_box2),
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
                            "legend": f"{st.session_state.select_box2}",
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
                # with mui.Card(key="realtimebox2", sx={"display": "flex", "flexDirection": "column"}):
                #     mui.CardHeader(title="实时数据", className="draggable")
                #     with mui.CardContent(sx={"flex": 1, "minHeight": 0}):
                #         split_dfs = split_dataframe_by_column(get_detected_data(resource_pool.update_timestamp),
                #                                               'monitor_id')

render_dashboard()
