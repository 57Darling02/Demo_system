import streamlit as st
import alert_suggestion_zsh as alert_suggestion
from ResourcePool import resource_pool
data = alert_suggestion.generate_alerts_and_suggestions(resource_pool.get_realtime_data())

@st.fragment
def show_form(item):
    with st.form(key=f"alert_{item['monitor_id']}"):
        st.write(f"Monitor ID: {item['monitor_id']}     collection time: {item['collect_time']}")
        if item["warnings"]:
            st.write("Warnings:")
            for warning in item["warnings"]:
                st.write(f"- {warning}")
        st.write("Suggestions:")
        for suggestion in item["suggestions"]:
            st.write(f"- {suggestion}")
        submit_button = st.form_submit_button(label='refresh')
        if submit_button:
            st.rerun()


for item in data:
    show_form(item)