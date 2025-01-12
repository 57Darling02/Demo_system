
import streamlit as st
class FixStreamlitElements(object):
    def __init__(self):
        pass
    def patch_modules_streamlit_elements(self, file: str, old_line: str, new_line: str):
        import streamlit_elements
        import os
        relative_file_path = "core/callback.py"
        library_root = list(streamlit_elements.__path__)[0]
        file_path = os.path.join(library_root, relative_file_path)
        with open(file_path, "r") as file:
            lines = file.readlines()
        is_changed = False
        for index, line in enumerate(lines):
            if old_line in line:
                print(f"Replacing line {index + 1} in {file_path}")
                lines[index] = line.replace(old_line, new_line)
                is_changed = True
        if is_changed:
            with open(file_path, "w") as file:
                file.writelines(lines)
            import importlib
            importlib.reload(streamlit_elements)
        return True
    # 修复 streamlit_elements 回调
    def patch_streamlit_elements(self):
        if st.button(label='开始修复 streamlit_elements 回调', type='primary'):
            # fix 1.34.0 修复官方提供的 自定义组件回调API
            self.patch_modules_streamlit_elements(
                "core/callback.py",
                "from streamlit.components.v1 import components",
                "from streamlit.components.v1 import custom_component as components\n",
            )
            # fix 1.40.0 修复 无效的转义序列
            self.patch_modules_streamlit_elements(
                "core/callback.py",
                'FORBIDDEN_PARAM_CHAR_RE = re.compile("\W+")',
                'FORBIDDEN_PARAM_CHAR_RE = re.compile(r"\W+")',
            )
            #fix 1.40.0 修复 会话状态 user_key 获取规则
            self.patch_modules_streamlit_elements(
                "core/callback.py",
                '        user_key = kwargs.get("user_key", None)\n',
                """
        try:
            user_key = None
            new_callback_data = kwargs[
                "ctx"
            ].session_state._state._new_session_state.get(
                "streamlit_elements.core.frame.elements_frame", None
            )
            if new_callback_data is not None:
                user_key = new_callback_data._key
        except:
            user_key = None
                """.rstrip()
                + "\n",
            )
            st.success('修复完成', icon='✅')
class FixStreamlitAntdComponents(object):
    def __init__(self):
        pass
    def patch_modules_streamlit_antd_components(self, file: str, old_code: str, new_code: str):
        import streamlit_antd_components
        import os
        relative_file_path = file
        library_root = list(streamlit_antd_components.__path__)[0]
        file_path = os.path.join(library_root, relative_file_path)
        # 替换逻辑
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        is_changed = False
        try:
            # 替换旧代码为新代码
            updated_content = content.replace(old_code, new_code)
            is_changed = True
        except Exception as e:
            print(e)
        if is_changed:
            # 写回文件
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(updated_content)
            import importlib
            importlib.reload(streamlit_antd_components)
        return True
    # 修复 streamlit_antd_components 回调
    def patch_streamlit_antd_components(self):
        if st.button(label='开始修复 streamlit_antd_components 回调', type='primary'):
            # fix 1.34.0 修复官方提供的 自定义组件回调API
            self.patch_modules_streamlit_antd_components(
                "utils/callback.py",
                "from streamlit.components.v1 import components as _components",
                "from streamlit.components.v1 import custom_component as _components",
            )
            #fix 1.40.0 修复 component 函数
            self.patch_modules_streamlit_antd_components(
                "utils/component_func.py",
                """
def component(id, kw, default=None, key=None):
    # repair component session init value
    if key is not None and key not in st.session_state:
        st.session_state[key] = default
    # pass component session state value to frontend
    if key is not None:
        # convert value
        st_value = convert_session_value(id, st.session_state[key], kw.get('kv'), kw.get('return_index'))
        kw.update({"stValue": st_value})
    else:
        kw.update({"stValue": None})
    return component_func(id=id, kw=json.loads(json.dumps(kw, cls=CustomEncoder)), default=default, key=key)
                """.rstrip(),
                """
def component(id, kw, default=None, key=None, on_change=None):
    if key is not None and key not in st.session_state:
        st.session_state[key] = default
    _on_change = None
    if on_change is not None:
        if key is None:
            st.error("You must pass a key if you want to use the on_change callback")
        else:
            def _on_change():
                return on_change(key)
    if key is not None:
        st_value = convert_session_value(
            id, st.session_state[key], kw.get('kv'), kw.get('return_index')
        )
        kw.update({"stValue": st_value})
    else:
        kw.update({"stValue": None})
    return component_func(
        id=id,
        kw=json.loads(json.dumps(kw, cls=CustomEncoder)),
        default=default,
        key=key,
        on_change=_on_change if _on_change is not None else None
    )
                """.rstrip()
                + "\n",
            )
            # fix 1.40.0 添加组件 on_change 参数
            for component_name in ['buttons', 'cascader', 'checkbox', 'chip', 'menu', 'rate', 'segmented', 'steps', 'switch', 'tabs', 'transfer', 'tree']:
                self.patch_modules_streamlit_antd_components(
                    f"widgets/{component_name}.py",
                    "return component(id=get_func_name(), kw=kw, default=default, key=key)",
                    "return component(id=get_func_name(), kw=kw, default=default, key=key, on_change=on_change)",
                )
            # fix 1.40.0 添加组件 on_change 参数
            for component_name in ['pagination']:
                self.patch_modules_streamlit_antd_components(
                    f"widgets/{component_name}.py",
                    "return component(id=get_func_name(), kw=update_kw(locals()), default=index, key=key)",
                    "return component(id=get_func_name(), kw=update_kw(locals()), default=index, key=key, on_change=on_change)",
                )
            st.success('修复完成', icon='✅')
if __name__ == "__main__":
    tabs = st.tabs(tabs=['streamlit-elements', 'streamlit-antd-components'])
    with tabs[0]:
        st.markdown(
            body='''
                ### 修复内容
                - 自 streamlit 1.34.0 起，官方提供提供了第三方组件专用回调 API `streamlit.components.v1.custom_component`，即修复官方提供的 自定义组件回调API
                - 适用 1.40.0 修复 无效的转义序列
                - 适用 1.40.0 修复 会话状态 user_key 获取规则
            ''',
            unsafe_allow_html=False
        )
        st.caption(
            body='''
                协作信息
                - 修改详情：参见源码部分 FixStreamlitElements
                - 修复技术创作人：bonajoy
                - 应用编辑创作人：六客叨叨
            '''
            )
        fse = FixStreamlitElements()
        fse.patch_streamlit_elements()

    with tabs[1]:
        st.markdown(
            body='''
                ### 修复内容
                - 自 streamlit 1.34.0 起，官方提供提供了第三方组件专用回调 API `streamlit.components.v1.custom_component`，即修复官方提供的 自定义组件回调API
                - 适用 1.40.0 修复 component 函数
                - 适用 1.40.0 修复 添加组件 on_change 参数
            ''',
            unsafe_allow_html=False
        )
        st.caption(
            body='''
                协作信息
                - 修改详情：参见源码部分 FixStreamlitAntdComponents
                - 修复技术创作人：ChazRuler、KuanHsiaoKuo
                - 应用编辑创作人：六客叨叨
            '''
            )
        fsac = FixStreamlitAntdComponents()
        fsac.patch_streamlit_antd_components()