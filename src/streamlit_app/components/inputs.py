from streamlit_app.utils import castors_possible_names, dainops_possible_names, ranguis_possible_names, \
    pios_possible_names, truk_possible_names

import pandas as pd
import streamlit as st


def add_new_cap(new_cap=None):
    if new_cap is None:
        new_cap = st.session_state.new_cap

    # Update caps list
    st.session_state.caps.append(new_cap)

    # Update caps_df
    st.session_state.caps_df = pd.concat([st.session_state.caps_df, pd.DataFrame({'cap': [new_cap]})])
    st.session_state.new_cap = ''

    # Update caps_preferences_df
    to_add_1 = pd.DataFrame({'cap': st.session_state.caps}).merge(
        pd.DataFrame({'cap_to_evaluate': [new_cap]}), how='cross')
    to_add_2 = to_add_1.rename(columns={'cap': 'cap_to_evaluate', 'cap_to_evaluate': 'cap'})
    st.session_state.caps_preferences_df = pd.concat(
        [st.session_state.caps_preferences_df, to_add_1, to_add_2]).fillna(0)

    # Update unitats_preferences_df
    to_add_1 = pd.DataFrame({'cap': [new_cap]}).merge(pd.DataFrame({'unitat_to_evaluate': st.session_state.unitats}),
                                                      how='cross')
    st.session_state.unitats_preferences_df = pd.concat([st.session_state.unitats_preferences_df, to_add_1])


def write_in_color(place, text, color='black', auto_detect_color=False):
    if auto_detect_color:
        if any(a in text for a in castors_possible_names):
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


def reset_table(to_reset):
    for element in to_reset:
        if type(st.session_state[element]) is list:
            st.session_state[element] = []
        else:
            # has to be pd.DataFrame
            st.session_state[element].drop(st.session_state[element].index, inplace=True)


def insert_info(table_name, col_to_add, col_to_match, match, key=None, extra_col_to_match=None, extra_match=None,
                value=None):
    assert value is not None or key is not None, 'Both value and key are None when inserting info!'
    element_to_add = st.session_state[key] if value is None else value
    element_to_add = element_to_add if type(element_to_add) is not list else ', '.join(element_to_add)
    if extra_col_to_match is None:
        st.session_state[table_name].loc[
            st.session_state[table_name][col_to_match] == match, col_to_add] = element_to_add
    else:
        st.session_state[table_name].loc[
            (st.session_state[table_name][col_to_match] == match) &
            (st.session_state[table_name][extra_col_to_match] == extra_match), col_to_add] = element_to_add


def add_new_unitat(key=None, value=None):
    if value is None:
        value = st.session_state[key]

    # Update unitats list
    st.session_state.unitats += [value]

    # Update unitats_df
    st.session_state.unitats_df = pd.concat([
        st.session_state.unitats_df,
        pd.DataFrame({
            'unitat': [value],
        })
    ])
    st.session_state.new_unitat = ''

    # Update unitats_preferences_df
    to_add_1 = pd.DataFrame({'unitat_to_evaluate': [value]}).merge(pd.DataFrame({'cap': st.session_state.caps}),
                                                                   how='cross')
    st.session_state.unitats_preferences_df = pd.concat([st.session_state.unitats_preferences_df, to_add_1])


def insert_multi_select(cap, sign, key):
    preferences_list = st.session_state[key]
    for cap_to_evaluate in preferences_list:
        st.session_state.caps_preferences_df.loc[
            (st.session_state.caps_preferences_df.cap == cap) &
            (st.session_state.caps_preferences_df.cap_to_evaluate == cap_to_evaluate)
            , 'preference'] += sign * 5


def introduce_unitats_preferences(place):
    unitats = st.session_state.unitats
    if len(unitats) == 0:
        place.write('Encara no hi ha cap unitat introduïda')
        return
    columns = place.columns(len(unitats) + 1)
    columns[0].write(f"**{'Cap'}**")
    for j, col in enumerate(columns):
        if j > 0:
            col.markdown(f"**{unitats[j - 1]}**")
    place.markdown('---')
    for i, cap in enumerate(st.session_state.caps):
        columns = place.columns(len(unitats) + 1)
        # TODO: centrar el nom
        columns[0].markdown(f'##')
        columns[0].write(cap)
        for j, col in enumerate(columns):
            if j > 0:
                unitat = unitats[j - 1]
                unitat_preference_key = f'unitat_preference_{i}_{j}'
                current_value = look_in_table('unitats_preferences_df', 'cap', cap, col_to_look='preference',
                                              extra_col_to_match='unitat_to_evaluate', extra_match=unitat)
                st.session_state[unitat_preference_key] = current_value if not pd.isnull(current_value) else 0
                col.slider(label='', min_value=0, max_value=5, step=1, key=unitat_preference_key,
                           on_change=insert_info,
                           kwargs={'table_name': 'unitats_preferences_df', 'col_to_add': 'preference',
                                   'col_to_match': 'cap', 'match': cap, 'key': unitat_preference_key,
                                   'extra_col_to_match': 'unitat_to_evaluate', 'extra_match': unitat})


def introduce_caps_preferences(place):
    caps = st.session_state.caps
    if not len(caps):
        place.write('Encara no hi ha cap cap introduït')
        return
    cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
    cap_col.markdown(f'**Cap**')
    positive_preferences.markdown(f'**Amb qui vol anar?**')
    negative_preferences.markdown(f'**Amb qui NO vol anar?**')
    for i, cap in enumerate(caps):
        cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
        cap_col.markdown(f'##')
        cap_col.write(cap)
        caps_to_evaluate = set(caps).difference({cap})
        # TODO: com fer que els valors seleccionats es mantinguin si canviem les pestanyes?

        positive_key = f'positive_caps_{i}'
        negative_key = f'negative_caps_{i}'

        st.session_state[positive_key] = st.session_state.caps_preferences_df.loc[
            (st.session_state.caps_preferences_df.cap == cap) &
            (st.session_state.caps_preferences_df.preference > 0),
            'cap_to_evaluate'
        ].values.tolist()
        st.session_state[negative_key] = st.session_state.caps_preferences_df.loc[
            (st.session_state.caps_preferences_df.cap == cap) &
            (st.session_state.caps_preferences_df.preference < 0),
            'cap_to_evaluate'
        ].values.tolist()

        positive_preferences.multiselect(label='', options=caps_to_evaluate, key=positive_key,
                                         on_change=insert_multi_select,
                                         kwargs={'sign': 1, 'cap': cap, 'key': positive_key})
        negative_preferences.multiselect(label='', options=caps_to_evaluate, key=negative_key,
                                         on_change=insert_multi_select,
                                         kwargs={'sign': -1, 'cap': cap, 'key': negative_key})


def introduce_caps_preferences_advanced(place):
    place.write('In construction..')


def inputs():
    st.header("Dades del Consell i l'agrupament")
    st.markdown(
        """
        En aquesta secció cal introduïr les següents dades de la tria de caps:
        """
    )

    # print_tables_for_debug()

    introduce_unitats_names = st.expander(label="Llista d'unitats")
    introduce_caps_names = st.expander(label="Llista de caps")
    st.markdown('---')
    unitats_preferences = st.expander(label="Preferències d'unitat")
    caps_preferences = st.expander(label="Preferències entre caps")
    caps_preferences_advanced = st.expander(label="Preferències avançades entre caps")

    introduce_unitats_list(place=introduce_unitats_names)
    introduce_caps_list(place=introduce_caps_names)
    introduce_unitats_preferences(place=unitats_preferences)
    introduce_caps_preferences(place=caps_preferences)
    introduce_caps_preferences_advanced(place=caps_preferences_advanced)


def print_tables_for_debug():
    raw_inputs = {
        'caps_df': st.session_state.caps_df,
        'unitats_df': st.session_state.unitats_df,
        'caps_preferences_df': st.session_state.caps_preferences_df,
        'unitats_preferences_df': st.session_state.unitats_preferences_df
    }
    for a, b in raw_inputs.items():
        st.write(a, b)


def insert_cau_normal():
    unitats = ['CiLL', 'LLiD', 'RiNG', 'PiC', 'Truk']
    for unitat in unitats:
        add_new_unitat(value=unitat)


def delete_unitat(unitat):
    st.session_state.unitats.remove(unitat)

    st.session_state.unitats_df = st.session_state.unitats_df[st.session_state.unitats_df.unitat != unitat]
    st.session_state.unitats_preferences_df = st.session_state.unitats_preferences_df[
        st.session_state.unitats_preferences_df.unitat != unitat]


def delete_cap(cap):
    st.session_state.caps.remove(cap)

    st.session_state.caps_df = st.session_state.caps_df[st.session_state.caps_df.cap != cap]
    st.session_state.unitats_preferences_df = st.session_state.unitats_preferences_df[
        st.session_state.unitats_preferences_df.cap != cap]
    st.session_state.caps_preferences_df = st.session_state.caps_preferences_df[
        (st.session_state.caps_preferences_df.cap != cap) & (
                st.session_state.caps_preferences_df.cap_to_evaluate != cap)]


def add_caps_lldg():
    caps_lldg = [
        ('Berta Zanuy', 4, 'Femení'),
        ('Helena Serra', 4, 'Femení'),
        ('Quim Rabella', 4, 'Masculí'),
        ('Clara Hosta', 4, 'Femení'),
        ('Eli Crego', 3, 'Femení'),
        ('Mateu Salvà', 3, 'Masculí'),
        ('Gina Pallares', 3, 'Femení'),
        ('Gerard Frigola', 3, 'Masculí'),
        ('Mia Losantos', 2, 'Femení'),
        ('Clara Estrada', 2, 'Femení'),
        ('Sara Bonal', 2, 'Femení'),
        ('Júlia Franquesa', 2, 'Femení'),
        ('Mar Rovira', 2, 'Femení'),
        ('Arnau Escolà', 1, 'Masculí'),
        ('Pol Mer', 1, 'Masculí'),
        ('Lluc Roda', 1, 'Masculí'),
        ('Marta Rovira', 1, 'Femení'),
        ('Simone Garcia', 1, 'Femení'),
        ('Maurici Rabella', 1, 'Masculí'),
        ('Max Font', 1, 'Masculí'),
    ]
    for cap, year, gender in caps_lldg:
        add_new_cap(new_cap=cap)
        insert_info(col_to_add='year', col_to_match='cap', match=cap, table_name='caps_df', value=year)
        insert_info(col_to_add='gender', col_to_match='cap', match=cap, table_name='caps_df', value=gender)


def look_in_table(table_name, col_to_match, match, col_to_look, extra_col_to_match=None, extra_match=None):
    if extra_col_to_match is None:
        return st.session_state[table_name].loc[
            st.session_state[table_name][col_to_match] == match,
            col_to_look
        ].iloc[0]
    else:
        return st.session_state[table_name].loc[
            (st.session_state[table_name][col_to_match] == match) &
            (st.session_state[table_name][extra_col_to_match] == extra_match),
            col_to_look
        ].iloc[0]


def introduce_unitats_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom de la unitat:', key='new_unitat', on_change=add_new_unitat, kwargs={'key': 'new_unitat'})
    col_2.markdown('##')
    col_2.button("Som un cau normal", key='cau_normal', help="S'afegiran les unitats: CiLL, LLiD, RiNG, PiC, Truk",
                 on_click=insert_cau_normal)
    col_3.write(f"Nombre d'unitats introduïdes: {len(st.session_state.unitats)}")
    col_3.button('Reset', key='reset_unitats', on_click=reset_table,
                 kwargs={'to_reset': ['unitats_df', 'unitats', 'unitats_preferences_df']})
    place.markdown('---')
    name_col, delete_col, min_caps, max_caps = place.columns(4)
    name_col.markdown('**Unitat**')
    min_caps.markdown('**Mínim de caps**')
    max_caps.markdown('**Màxim de caps**')
    for i, unitat in enumerate(st.session_state.unitats):
        name_col, delete_col, min_caps, max_caps = place.columns(4)
        name_col.markdown(f'##')
        write_in_color(name_col, unitat, auto_detect_color=True)
        delete_col.button('Esborra', on_click=delete_unitat, key=f'delete_unitat_{i}',
                          kwargs={'unitat': unitat})

        min_caps_key = f'min_caps_{i}'
        max_caps_key = f'max_caps_{i}'
        st.session_state[min_caps_key] = look_in_table('unitats_df', 'unitat', unitat, 'min_caps')
        st.session_state[max_caps_key] = look_in_table('unitats_df', 'unitat', unitat, 'max_caps')

        min_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'min_caps', 'col_to_match': 'unitat', 'match': unitat,
                                      'key': min_caps_key, 'table_name': 'unitats_df'}, key=f'min_caps_{i}',
                              help='mínim de caps per portar la unitat?')
        max_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'max_caps', 'col_to_match': 'unitat', 'match': unitat,
                                      'key': max_caps_key, 'table_name': 'unitats_df'}, key=f'max_caps_{i}',
                              help='màxim de caps per portar la unitat?')


def introduce_caps_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom del/la cap:', key='new_cap', on_change=add_new_cap)
    # TODO: alguna manera de no haver d'escriure els caps tota l'estona?
    col_2.button('Som AE Lluïsos de Gràcia', on_click=add_caps_lldg)
    col_3.button('Reset', key='reset_names', on_click=reset_table,
                 kwargs={'to_reset': ['caps_df', 'caps', 'caps_preferences_df']})
    col_3.write(f"Nombre de caps introduïts: {len(st.session_state.caps)}")
    place.markdown('---')
    name_col, delete_col, any_col, gender_col, experience_col = place.columns(5)
    name_col.markdown('**Nom**')
    any_col.markdown('**Anys**')
    gender_col.markdown('**Gènere**')
    experience_col.markdown('**Experiència**')
    for i, cap in enumerate(st.session_state.caps):
        name_col, delete_col, any_col, gender_col, experience_col = place.columns(5)
        name_col.markdown(f'##')
        write_in_color(name_col, cap, 'gray')
        delete_col.button('Esborra', on_click=delete_cap, key=f'delete_cap_{i}',
                          kwargs={'cap': cap})
        year_key = f'year_value_{i}'
        gender_key = f'gender_value_{i}'
        experience_key = f'experience_number_{i}'
        st.session_state[year_key] = look_in_table('caps_df', 'cap', cap, 'year')
        st.session_state[gender_key] = look_in_table('caps_df', 'cap', cap, 'gender')
        exp_state = look_in_table('caps_df', 'cap', cap, 'experience')
        st.session_state[experience_key] = [] if pd.isnull(exp_state) else exp_state.split(', ')

        any_col.number_input('', min_value=1, max_value=10, on_change=insert_info,
                             kwargs={'col_to_add': 'year', 'col_to_match': 'cap', 'match': cap,
                                     'key': year_key, 'table_name': 'caps_df'}, key=year_key,
                             help='és cap de 1r, 2n, 3r any...')
        gender_col.selectbox('', options=['Femení', 'Masculí', 'Altres'], on_change=insert_info,
                             kwargs={'col_to_add': 'gender', 'col_to_match': 'cap', 'match': cap,
                                     'key': gender_key, 'table_name': 'caps_df'}, key=gender_key)
        current_unitats = st.session_state.unitats_df.unitat.unique().tolist()
        help_message = "L'OPTIMITZADOR ENCARA NO HO SUPORTA. " \
                       "quines unitats ha portat altres anys? Omple abans la llista d'unitats"
        experience_col.multiselect(label='', options=current_unitats, on_change=insert_info,
                                   kwargs={'col_to_add': 'experience', 'col_to_match': 'cap', 'match': cap,
                                           'key': experience_key, 'table_name': 'caps_df'},
                                   key=experience_key, help=help_message, disabled=True)
