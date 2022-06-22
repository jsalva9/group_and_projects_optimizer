from components.intro import intro
from components.inputs import inputs
import streamlit as st

if __name__ == '__main__':
    st.set_page_config(page_title='Assistent de la tria de caps · Streamlit', page_icon=None, layout="wide", initial_sidebar_state="auto",
                       menu_items=None)
    # intro()
    inputs()

