from streamlit_app.components.intro import intro
from streamlit_app.components.inputs import inputs
from streamlit_app.components.optimizer import optimizer
import streamlit as st


def main():
    st.set_page_config(page_title='Assistent de la tria de caps · Streamlit', page_icon=None, layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)
    st.sidebar.selectbox("Pàgina", ["Inputs", "Introducció", "Inputs", "Optimitzador"], key='current_page')
    if st.session_state.current_page == 'Introducció':
        intro()
    if st.session_state.current_page == 'Inputs':
        inputs()
    if st.session_state.current_page == 'Optimitzador':
        optimizer()
