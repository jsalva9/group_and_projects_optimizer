from components.intro import intro
from components.inputs import inputs
from components.optimizer import optimizer
import streamlit as st

if __name__ == '__main__':
    st.set_page_config(page_title='Assistent de la tria de caps · Streamlit', page_icon=None, layout="wide", initial_sidebar_state="auto",
                       menu_items=None)
    # st.sidebar.header('Pàgina')
    st.sidebar.selectbox("Pàgina", ["Inputs", "Introducció", "Inputs", "Optimitzador"], key='current_page')
    if st.session_state.current_page == 'Introducció':
        intro()
    if st.session_state.current_page == 'Inputs':
        inputs()
    if st.session_state.current_page == 'Optimizer':
        optimizer()

