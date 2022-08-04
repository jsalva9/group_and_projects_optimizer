from streamlit_app.components.intro import intro
from streamlit_app.components.inputs import inputs
from streamlit_app.components.optimizer import optimizer
import streamlit as st
import pandas as pd


def create_table(table_name, cols):
    table = pd.DataFrame()
    for col in cols:
        table[col] = []
    st.session_state[table_name] = table


def main():
    st.set_page_config(page_title='Assistent de la tria de caps · Streamlit', page_icon=None, layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)
    st.sidebar.selectbox("Pàgina", ["Introducció", "Inputs", "Optimitzador"], key='current_page')

    def initialize_session_state():
        if 'caps' not in st.session_state:
            st.session_state.caps = []
        if 'unitats' not in st.session_state:
            st.session_state.unitats = []
        if 'caps_df' not in st.session_state:
            create_table('caps_df', ['cap', 'year', 'gender', 'experience'])
        if 'unitats_df' not in st.session_state:
            create_table('unitats_df', ['unitat', 'min_caps', 'max_caps'])
        if 'unitats_preferences_df' not in st.session_state:
            create_table('unitats_preferences_df',
                         ['cap', 'unitat_to_evaluate', 'positive_preference', 'negative_preference'])
        if 'caps_preferences_df' not in st.session_state:
            create_table('caps_preferences_df',
                         ['cap', 'cap_to_evaluate', 'positive_preference', 'negative_preference'])
        if 'fixed_caps' not in st.session_state:
            st.session_state.fixed_caps = {}

    initialize_session_state()

    if st.session_state.current_page == 'Introducció':
        intro()
    if st.session_state.current_page == 'Inputs':
        inputs()
    if st.session_state.current_page == 'Optimitzador':
        optimizer()
