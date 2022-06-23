import warnings
from streamlit_app.utils import castors_possible_names, dainops_possible_names, ranguis_possible_names, pios_possible_names, truk_possible_names

import pandas as pd
import streamlit as st


def add_new_cap():
    st.session_state.caps_df = pd.concat([
        st.session_state.caps_df,
        pd.DataFrame({
            'cap': [st.session_state.new_cap],
            'year': [pd.NA],
            'gender': [pd.NA]
        })
    ]).reset_index(drop=True)
    st.session_state.new_cap = ''


def write_in_color(place, text, color='black', auto_detect_color=False):
    if auto_detect_color:
        if any(a in text for a in castors_possible_names
               ):
            color = 'orange'
        elif any(a in text for a in dainops_possible_names):
            color = 'yellow'
        elif any(a in text for a in ranguis_possible_names):
            color = 'blue'
        elif any(a in text for a in pios_possible_names):
            color = 'red'
        elif any(a in text for a in truk_possible_names):
            color = 'green'

    place.markdown(f'<span style="color:{color}">{text}</span>', unsafe_allow_html=True)


def delete_last_entry(table_name):
    st.session_state[table_name] = st.session_state[table_name][:-1]


def reset_table(table_name):
    st.session_state[table_name].drop(st.session_state.caps_df.index, inplace=True)


def insert_info(table_name, col_to_add, col_to_match, match, key):
    element_to_add = st.session_state[key] if type(st.session_state[key]) is not list else ', '.join(
        st.session_state[key])
    st.session_state[table_name].loc[
        st.session_state[table_name][col_to_match] == match, col_to_add] = element_to_add


def create_caps_df():
    st.session_state.caps_df = pd.DataFrame({
        'cap': [],
        'year': [],
        'gender': [],
        'experience': []
    })


def create_unitats_df():
    st.session_state.unitats_df = pd.DataFrame({
        'unitat': [],
        'min_caps': [],
        'max_caps': []
    })


def add_new_unitat():
    st.session_state.unitats_df = pd.concat([
        st.session_state.unitats_df,
        pd.DataFrame({
            'unitat': [st.session_state.new_unitat],
            'min_caps': [pd.NA],
            'max_caps': [pd.NA]
        })
    ]).reset_index(drop=True)
    st.session_state.new_unitat = ''


def inputs():
    st.subheader('Dades del problema')
    st.markdown(
        """
        En aquesta secció cal proporcionar les dades del problema
        """
    )

    initialize_session_state()

    introduce_unitats_names = st.expander(label="Introdueix aquí les diferents unitats")
    introduce_caps_names = st.expander(label="Introdueix aquí la llista de caps")

    introduce_unitats_list(place=introduce_unitats_names)
    introduce_caps_list(place=introduce_caps_names)

    # elif st.session_state.step == 'unitats_preferences':
    #     st.markdown("### A continuació s'especifiquen les preferències d'unitats")
    #     pass
    #
    # elif st.session_state.step == 'caps_preferences':
    #     st.markdown("### A continuació s'especifiquen les preferències de caps")
    #     pass
    #
    # elif st.session_state.step == 'pause':
    #     st.session_state.step = st.session_state.after_pause


def initialize_session_state():
    if 'caps_df' not in st.session_state:
        create_caps_df()
    if 'unitats_df' not in st.session_state:
        create_unitats_df()
    if 'step' not in st.session_state:
        # Steps: ['caps_list', 'unitats_list', 'unitats_preferences', 'caps_preferences']
        st.session_state.step = 'caps_list'


def introduce_unitats_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom de la unitat:', key='new_unitat', on_change=add_new_unitat)
    col_2.button('Esborra el darrer nom', key='delete_last_unitat', on_click=delete_last_entry,
                 kwargs={'table_name': 'unitats_df'})
    col_2.button('Reset', key='reset_unitats', on_click=reset_table, kwargs={'table_name': 'unitats_df'})
    col_3.write(f"Nombre d'unitats introduïdes: {len(st.session_state.unitats_df.index)}")
    place.markdown('---')
    name_col, min_caps, max_caps = place.columns([1, 1, 1])
    name_col.markdown('**Unitat**')
    min_caps.markdown('**Mínim de caps**')
    max_caps.markdown('**Màxim de caps**')
    for i, row in st.session_state.unitats_df.iterrows():
        name_col, min_caps, max_caps = place.columns([1, 1, 1])
        name_col.markdown(f'##')
        write_in_color(name_col, row.unitat, None, auto_detect_color=True)

        min_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'year', 'col_to_match': 'unitat', 'match': row.unitat,
                                      'key': f'min_caps_{i}', 'table_name': 'unitats_df'}, key=f'min_caps_{i}',
                              help='mínim de caps per portar la unitat?')
        max_caps.selectbox('', options=['0', '1', '2'], on_change=insert_info,
                           kwargs={'col_to_add': 'gender', 'col_to_match': 'unitat', 'match': row.unitat,
                                   'key': f'max_caps_{i}', 'table_name': 'unitats_df'}, key=f'max_caps_{i}',
                           help='màxim de caps per portar la unitat?')


def introduce_caps_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom del/la cap:', key='new_cap', on_change=add_new_cap)
    col_2.button('Esborra el darrer nom', key='delete_last_name', on_click=delete_last_entry,
                 kwargs={'table_name': 'caps_df'})
    col_2.button('Reset', key='reset_names', on_click=reset_table, kwargs={'table_name': 'caps_df'})
    col_3.write(f"Nombre de caps introduïts: {len(st.session_state.caps_df.index)}")
    place.markdown('---')
    name_col, any_col, gender_col, experience_col = place.columns(4)
    name_col.markdown('**Nom**')
    any_col.markdown('**Anys**')
    gender_col.markdown('**Gènere**')
    experience_col.markdown('**Experiència**')
    for i, row in st.session_state.caps_df.iterrows():
        name_col, any_col, gender_col, experience_col = place.columns(4)
        name_col.markdown(f'##')
        write_in_color(name_col, row.cap, 'gray')
        any_col.number_input('', min_value=1, max_value=10, on_change=insert_info,
                             kwargs={'col_to_add': 'year', 'col_to_match': 'cap', 'match': row.cap,
                                     'key': f'year_value_{i}', 'table_name': 'caps_df'}, key=f'year_value_{i}',
                             help='és cap de 1r, 2n, 3r any...')
        gender_col.selectbox('', options=['Femení', 'Masculí', 'Altres'], on_change=insert_info,
                             kwargs={'col_to_add': 'gender', 'col_to_match': 'cap', 'match': row.cap,
                                     'key': f'gender_value_{i}', 'table_name': 'caps_df'}, key=f'gender_value_{i}')
        current_unitats = st.session_state.unitats_df.unitat.unique().tolist()
        help_message = "quines unitats ha portat altres anys? Omple abans la llista d'unitats"
        experience_col.multiselect(label='', options=current_unitats, on_change=insert_info,
                                   kwargs={'col_to_add': 'experience', 'col_to_match': 'cap', 'match': row.cap,
                                           'key': f'experience_number_{i}', 'table_name': 'caps_df'},
                                   key=f'experience_number_{i}', help=help_message)
