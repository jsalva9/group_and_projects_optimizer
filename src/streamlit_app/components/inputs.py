import warnings

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


def delete_last_entry(table_name):
    st.session_state[table_name] = st.session_state[table_name][:-1]


def reset_table(table_name):
    st.session_state[table_name].drop(st.session_state.caps_df.index, inplace=True)


def insert_info(table_name, col_to_add, col_to_match, match, key):
    st.session_state[table_name].loc[
        st.session_state[table_name][col_to_match] == match, col_to_add] = st.session_state[key]


def create_caps_df():
    st.session_state.caps_df = pd.DataFrame({
        'cap': [],
        'year': [],
        'gender': []
    })


def create_unitats_df():
    st.session_state.unitats_df = pd.DataFrame({
        'unitat': [],
        'min_caps': [],
        'max_caps': []
    })


def go_back_or_forward(key):
    if key == 'confirm_caps':
        st.session_state.state = 'unitats_list'
    else:
        st.session_state.state = 'caps_list'


def submit_names(container_1, container_2):
    st.session_state.state = 'pause'
    if len(st.session_state.caps_df.index) == 0:
        st.write('No hi ha caps registrats!')
    else:
        st.write('Taula de caps registrada: ')
        st.dataframe(st.session_state.caps_df)
    yes, no = st.columns(2)
    yes.button('Endavant!', key='confirm_caps', on_click=go_back_or_forward, kwargs={'key': 'confirm_caps'})
    no.button('Tornar enrere per revisar la taula', key='revise_caps', on_click=go_back_or_forward,
              kwargs={'key': 'revise_caps'})


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


def submit_unitats(container):
    st.session_state.step = 'unitats_preferences'
    if len(st.session_state.unitats_df.index) == 0:
        container.write('No hi ha unitats registrades!')
    else:
        container.write("Taula d'unitats registrada: ")
        container.dataframe(st.session_state.unitats_df)


def inputs():
    st.subheader('Dades del problema')
    st.markdown(
        """
        En aquesta secció cal proporcionar les dades del problema
        """
    )

    initialize_session_state()

    if st.session_state.step == 'caps_list':
        introduce_caps_list()

    elif st.session_state.step == 'unitats_list':
        introduce_unitats_list()

    elif st.session_state.step == 'unitats_preferences':
        st.markdown("### A continuació s'especifiquen les preferències d'unitats")

        pass
    elif st.session_state.step == 'caps_preferences':
        st.markdown("### A continuació s'especifiquen les preferències de caps")

        pass
    elif st.session_state.step == 'pause':
        st.session_state.step = st.session_state.after_pause


def initialize_session_state():
    if 'caps_df' not in st.session_state:
        create_caps_df()
    if 'unitats_df' not in st.session_state:
        create_unitats_df()
    if 'step' not in st.session_state:
        # Steps: ['caps_list', 'unitats_list', 'unitats_preferences', 'caps_preferences']
        st.session_state.step = 'caps_list'


def introduce_unitats_list():
    st.markdown("### A continuació s'especifica la llista d'unitats")
    problem_inputs = st.container()
    problem_info = st.container()
    problem_inputs.text_input('Nom de la unitat:', key='new_unitat', on_change=add_new_unitat)
    col1, col2, col3, _ = problem_inputs.columns([2, 1, 1, 1])
    col1.button('Esborra el darrer nom', key='delete_last_unitat', on_click=delete_last_entry,
                kwargs={'table_name': 'unitats_df'})
    col2.button('Reset', key='reset_unitats', on_click=reset_table, kwargs={'table_name': 'unitats_df'})
    col3.button('Submit', key='submit_unitats', on_click=submit_unitats, kwargs={'container': problem_info})
    name_col, min_caps, max_caps = problem_info.columns([1, 1, 1])
    name_col.markdown('**Unitat**')
    min_caps.markdown('**Mínim de caps**')
    max_caps.markdown('**Màxim de caps**')
    for i, row in st.session_state.unitats_df.iterrows():
        name_col, min_caps, max_caps = problem_info.columns([1, 1, 1])
        name_col.markdown(f'##')
        name_col.markdown(f'**{row.unitat}**')
        min_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'year', 'col_to_match': 'unitat', 'match': row.unitat,
                                      'key': f'min_caps_{i}', 'table_name': 'unitats_df'}, key=f'min_caps_{i}',
                              help='mínim de caps per portar la unitat?')
        max_caps.selectbox('', options=['0', '1', '2'], on_change=insert_info,
                           kwargs={'col_to_add': 'gender', 'col_to_match': 'unitat', 'match': row.unitat,
                                   'key': f'max_caps_{i}', 'table_name': 'unitats_df'}, key=f'max_caps_{i}',
                           help='màxim de caps per portar la unitat?')


def introduce_caps_list():
    st.markdown("### A continuació s'especifica la llista de caps")
    problem_inputs = st.container()
    problem_info = st.container()
    problem_inputs.text_input('Nom del/la cap:', key='new_cap', on_change=add_new_cap)
    col1, col2, col3, _ = problem_inputs.columns([2, 1, 1, 1])
    col1.button('Esborra el darrer nom', key='delete_last_name', on_click=delete_last_entry,
                kwargs={'table_name': 'caps_df'})
    col2.button('Reset', key='reset_names', on_click=reset_table, kwargs={'table_name': 'caps_df'})
    col3.button('Submit', key='submit_names', on_click=submit_names,
                kwargs={'container_1': problem_info, 'container_2': problem_inputs})
    name_col, any_col, gender_col = problem_info.columns([1, 1, 1])
    name_col.markdown('**Nom**')
    any_col.markdown('**Anys**')
    gender_col.markdown('**Gènere**')
    for i, row in st.session_state.caps_df.iterrows():
        name_col, any_col, gender_col = problem_info.columns([1, 1, 1])
        name_col.markdown(f'##')
        name_col.markdown(f'**{row.cap}**')
        any_col.number_input('', min_value=1, max_value=10, on_change=insert_info,
                             kwargs={'col_to_add': 'year', 'col_to_match': 'cap', 'match': row.cap,
                                     'key': f'year_value_{i}', 'table_name': 'caps_df'}, key=f'year_value_{i}',
                             help='és cap de 1r, 2n, 3r any...')
        gender_col.selectbox('', options=['0', '1', '2'], on_change=insert_info,
                             kwargs={'col_to_add': 'gender', 'col_to_match': 'cap', 'match': row.cap,
                                     'key': f'gender_value_{i}', 'table_name': 'caps_df'}, key=f'gender_value_{i}',
                             help='identifica amb el mateix nombre les persones del mateix gènere')
