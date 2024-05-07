import streamlit as st


def create_components(component_info):
    user_inputs = {}
    for key, value in component_info.items():
        title = key.replace('_', ' ').title()
        if value['type'] == 'text':
            user_inputs[value['name']] = st.text_input(title, key=key)
        elif value['type'] == 'radio':
            user_inputs[value['name']] = st.radio(title, value['options'], key=key)
        elif value['type'] == 'selectbox':
            user_inputs[value['name']] = st.selectbox(title, value['options'], key=key)
        elif value['type'] == 'text_area':
            user_inputs[value['name']] = st.text_area(title, key=key)
    return user_inputs

def go_back():
    st.session_state['current_screen'] = 'start'