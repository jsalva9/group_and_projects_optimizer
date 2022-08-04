import pandas as pd
import streamlit as st
from streamlit_app.utils import custom_write, endline, caps_lldg, POSITIVE_WEIGHT, NEGATIVE_WEIGHT


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


def reset_table(to_reset):
    for element in to_reset:
        if type(st.session_state[element]) is list:
            st.session_state[element] = []
        elif type(st.session_state[element]) is pd.DataFrame:
            st.session_state[element].drop(st.session_state[element].index, inplace=True)
        elif type(st.session_state[element]) is dict:
            st.session_state[element] = {}
        else:
            assert False, f'Trying to reset {element}, an element of type {type(element)}. ' \
                          f'It is not a list, pd.DataFrame or dictionary'


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

    # Update fixed_caps
    st.session_state.fixed_caps[value] = []


def insert_multi_select(cap, sign, key, level):
    preferences_list = st.session_state[key]
    table = f'{level}s_preferences_df'
    thing_to_evaluate = f'{level}_to_evaluate'
    pref_col = 'positive_preference' if sign > 0 else 'negative_preference'
    st.session_state[table].loc[
        (st.session_state[table].cap == cap)
        , pref_col] = 0
    for cap_to_evaluate in preferences_list:
        st.session_state[table].loc[
            (st.session_state[table].cap == cap) &
            (st.session_state[table][thing_to_evaluate] == cap_to_evaluate)
            , pref_col] += sign * POSITIVE_WEIGHT if sign > 0 else sign * NEGATIVE_WEIGHT


def introduce_unitats_preferences(place):
    unitats = st.session_state.unitats
    if len(unitats) == 0:
        place.write('Encara no hi ha cap unitat introduïda')
        return
    columns = place.columns(len(unitats) + 1)
    for j, col in enumerate(columns):
        if j > 0:
            custom_write(col, str(unitats[j - 1]), bold=True, align='center', auto_detect_color=True)
    place.markdown('---')
    for i, cap in enumerate(st.session_state.caps):
        columns = place.columns(len(unitats) + 1)
        # TODO: centrar el nom
        columns[0].markdown(f'##')
        custom_write(columns[0], cap, align='center')
        for j, col in enumerate(columns):
            if j > 0:
                unitat = unitats[j - 1]
                unitat_preference_key = f'unitat_preference_{i}_{j}'
                current_value = look_in_table('unitats_preferences_df', 'cap', cap, col_to_look='preference',
                                              extra_col_to_match='unitat_to_evaluate', extra_match=unitat)
                st.session_state[unitat_preference_key] = current_value if current_value is not None else 0
                col.slider(label='', min_value=0, max_value=5, step=1, key=unitat_preference_key,
                           on_change=insert_info,
                           kwargs={'table_name': 'unitats_preferences_df', 'col_to_add': 'preference',
                                   'col_to_match': 'cap', 'match': cap, 'key': unitat_preference_key,
                                   'extra_col_to_match': 'unitat_to_evaluate', 'extra_match': unitat})


def introduce_unitats_preferences_new(place):
    explanation = 'Les unitats que no són preferides ni vetades són aquelles a les quals estaries disposat a anar.'
    custom_write(place, explanation)
    endline(place)

    unitats = st.session_state.unitats
    caps = st.session_state.caps
    if len(unitats) == 0:
        place.warning('Encara no hi ha cap unitat introduïda')
        return
    if len(caps) == 0:
        place.warning('Encara no hi ha caps introduïts')
        return

    cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
    #TODO: explicar que si no s'especifica res, hi podries anar
    custom_write(positive_preferences, 'Unitats preferides', align='center', bold=True)
    custom_write(negative_preferences, 'Unitats vetades', align='center', bold=True)

    for i, cap in enumerate(caps):
        cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
        endline(cap_col)
        custom_write(cap_col, cap, align='center', color='grey')
        unitats_to_evaluate = set(unitats)

        positive_key = f'positive_unitats_{i}'
        negative_key = f'negative_unitats_{i}'

        current_positive = st.session_state.unitats_preferences_df.loc[
            (st.session_state.unitats_preferences_df.cap == cap) &
            (st.session_state.unitats_preferences_df.positive_preference > 0),
            'unitat_to_evaluate'
        ].values.tolist()
        current_negative = st.session_state.unitats_preferences_df.loc[
            (st.session_state.unitats_preferences_df.cap == cap) &
            (st.session_state.unitats_preferences_df.negative_preference < 0),
            'unitat_to_evaluate'
        ].values.tolist()

        positive_preferences.multiselect(label='', options=unitats_to_evaluate, key=positive_key,
                                         on_change=insert_multi_select, default=current_positive,
                                         kwargs={'sign': 1, 'cap': cap, 'key': positive_key, 'level': 'unitat'})
        negative_preferences.multiselect(label='', options=unitats_to_evaluate, key=negative_key,
                                         on_change=insert_multi_select, default=current_negative,
                                         kwargs={'sign': -1, 'cap': cap, 'key': negative_key, 'level': 'unitat'})


def introduce_caps_preferences(place):
    caps = st.session_state.caps
    if not len(caps):
        place.write('Encara no hi ha cap cap introduït')
        return
    cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
    custom_write(positive_preferences, 'Amb qui vol anar', align='center', bold=True)
    custom_write(negative_preferences, 'Amb qui NO vol anar', align='center', bold=True)
    for i, cap in enumerate(caps):
        cap_col, positive_preferences, negative_preferences = place.columns([1, 1.5, 1.5])
        endline(cap_col)
        custom_write(cap_col, cap, align='center', color='grey')
        caps_to_evaluate = set(caps).difference({cap})

        positive_key = f'positive_caps_{i}'
        negative_key = f'negative_caps_{i}'

        current_positive = st.session_state.caps_preferences_df.loc[
            (st.session_state.caps_preferences_df.cap == cap) &
            (st.session_state.caps_preferences_df.positive_preference > 0),
            'cap_to_evaluate'
        ].values.tolist()
        current_negative = st.session_state.caps_preferences_df.loc[
            (st.session_state.caps_preferences_df.cap == cap) &
            (st.session_state.caps_preferences_df.negative_preference < 0),
            'cap_to_evaluate'
        ].values.tolist()

        positive_preferences.multiselect(label='', options=caps_to_evaluate, key=positive_key,
                                         on_change=insert_multi_select, default=current_positive,
                                         kwargs={'sign': 1, 'cap': cap, 'key': positive_key, 'level': 'cap'})
        negative_preferences.multiselect(label='', options=caps_to_evaluate, key=negative_key,
                                         on_change=insert_multi_select, default=current_negative,
                                         kwargs={'sign': -1, 'cap': cap, 'key': negative_key, 'level': 'cap'})


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
    introduce_unitats_preferences_new(place=unitats_preferences)
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
    if unitat in st.session_state.unitats:
        st.session_state.unitats.remove(unitat)

    st.session_state.unitats_df = st.session_state.unitats_df[st.session_state.unitats_df.unitat != unitat]
    st.session_state.unitats_preferences_df = st.session_state.unitats_preferences_df[
        st.session_state.unitats_preferences_df.unitat_to_evaluate != unitat]

    del st.session_state.fixed_caps[unitat]


def delete_cap(cap):
    if cap in st.session_state.caps:
        st.session_state.caps.remove(cap)

    st.session_state.caps_df = st.session_state.caps_df[st.session_state.caps_df.cap != cap]
    st.session_state.unitats_preferences_df = st.session_state.unitats_preferences_df[
        st.session_state.unitats_preferences_df.cap != cap]
    st.session_state.caps_preferences_df = st.session_state.caps_preferences_df[
        (st.session_state.caps_preferences_df.cap != cap) & (
                st.session_state.caps_preferences_df.cap_to_evaluate != cap)]


def add_caps_lldg():

    for cap, year, gender in caps_lldg:
        add_new_cap(new_cap=cap)
        insert_info(col_to_add='year', col_to_match='cap', match=cap, table_name='caps_df', value=year)
        insert_info(col_to_add='gender', col_to_match='cap', match=cap, table_name='caps_df', value=gender)


def look_in_table(table_name, col_to_match, match, col_to_look, extra_col_to_match=None, extra_match=None):
    if extra_col_to_match is None:
        ans = st.session_state[table_name].loc[
            st.session_state[table_name][col_to_match] == match,
            col_to_look
        ].iloc[0]
    else:
        ans = st.session_state[table_name].loc[
            (st.session_state[table_name][col_to_match] == match) &
            (st.session_state[table_name][extra_col_to_match] == extra_match),
            col_to_look
        ].iloc[0]
    return None if pd.isnull(ans) else ans


def introduce_unitats_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom de la unitat:', key='new_unitat', on_change=add_new_unitat, kwargs={'key': 'new_unitat'})
    col_2.markdown('##')
    col_2.button("Som un cau normal", key='cau_normal', help="S'afegiran les unitats: CiLL, LLiD, RiNG, PiC, Truk",
                 on_click=insert_cau_normal)
    col_3.write(f"Nombre d'unitats introduïdes: {len(st.session_state.unitats)}")
    col_3.button('Reset', key='reset_unitats', on_click=reset_table,
                 kwargs={'to_reset': ['unitats_df', 'unitats', 'unitats_preferences_df', 'fixed_caps']})
    place.markdown('---')
    name_col, delete_col, min_caps, max_caps = place.columns(4)
    custom_write(name_col, 'Unitat', align='right', bold=True)
    custom_write(min_caps, 'Mínim de caps', align='center', bold=True)
    custom_write(max_caps, 'Màxim de caps', align='center', bold=True)
    for i, unitat in enumerate(st.session_state.unitats):
        name_col, delete_col, min_caps, max_caps = place.columns(4)
        endline(name_col)
        custom_write(name_col, unitat, align='right', auto_detect_color=True)
        endline(delete_col)
        delete_col.button('Esborra', on_click=delete_unitat, key=f'delete_unitat_{i}',
                          kwargs={'unitat': unitat})

        min_caps_key = f'min_caps_{i}'
        max_caps_key = f'max_caps_{i}'
        current_min_caps = look_in_table('unitats_df', 'unitat', unitat, 'min_caps')
        if current_min_caps is None:
            current_min_caps = 2
        current_max_caps = look_in_table('unitats_df', 'unitat', unitat, 'max_caps')
        if current_max_caps is None:
            current_max_caps = 6

        min_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'min_caps', 'col_to_match': 'unitat', 'match': unitat,
                                      'key': min_caps_key, 'table_name': 'unitats_df'}, key=min_caps_key,
                              help='mínim de caps per portar la unitat?', value=int(current_min_caps))
        max_caps.number_input('', min_value=1, max_value=10, on_change=insert_info,
                              kwargs={'col_to_add': 'max_caps', 'col_to_match': 'unitat', 'match': unitat,
                                      'key': max_caps_key, 'table_name': 'unitats_df'}, key=max_caps_key,
                              help='màxim de caps per portar la unitat?', value=int(current_max_caps))


def introduce_caps_list(place):
    col_1, col_2, col_3 = place.columns([2, 2, 1.5])

    col_1.text_input('Nom del/la cap:', key='new_cap', on_change=add_new_cap)
    # TODO: alguna manera de no haver d'escriure els caps tota l'estona?
    col_2.button("Som l'AE Lluïsos de Gràcia", on_click=add_caps_lldg)
    col_3.button('Reset', key='reset_names', on_click=reset_table,
                 kwargs={'to_reset': ['caps_df', 'caps', 'caps_preferences_df']})
    col_3.write(f"Nombre de caps introduïts: {len(st.session_state.caps)}")
    place.markdown('---')
    name_col, delete_col, any_col, gender_col, experience_col = place.columns(5)
    custom_write(name_col, 'Nom', bold=True, align='right')
    custom_write(any_col, 'Anys', bold=True, align='center')
    custom_write(gender_col, 'Gènere', bold=True, align='center')
    custom_write(experience_col, 'Experiència', bold=True, align='center')
    for i, cap in enumerate(st.session_state.caps):
        name_col, delete_col, any_col, gender_col, experience_col = place.columns(5)
        endline(name_col)
        custom_write(name_col, cap, color='gray', align='right')
        endline(delete_col)
        delete_col.button('Esborra', on_click=delete_cap, key=f'delete_cap_{i}',
                          kwargs={'cap': cap})
        year_key = f'year_value_{i}'
        gender_key = f'gender_value_{i}'
        experience_key = f'experience_number_{i}'
        current_year = look_in_table('caps_df', 'cap', cap, 'year')
        current_gender = look_in_table('caps_df', 'cap', cap, 'gender')
        if current_gender is not None:
            st.session_state[gender_key] = current_gender
        # exp_state = look_in_table('caps_df', 'cap', cap, 'experience')
        # st.session_state[experience_key] = [] if pd.isnull(exp_state) else exp_state.split(', ')

        any_col.number_input('', min_value=1, max_value=10, on_change=insert_info,
                             kwargs={'col_to_add': 'year', 'col_to_match': 'cap', 'match': cap,
                                     'key': year_key, 'table_name': 'caps_df'}, key=year_key,
                             help='és cap de 1r, 2n, 3r any...',
                             value=int(current_year) if current_year is not None else 1)
        gender_options = ['Femení', 'Masculí', 'Altres']
        index = gender_options.index(current_gender) if current_gender is not None else 0
        gender_col.selectbox('', options=gender_options, on_change=insert_info,
                             kwargs={'col_to_add': 'gender', 'col_to_match': 'cap', 'match': cap,
                                     'key': gender_key, 'table_name': 'caps_df'}, key=gender_key, index=index)
        current_unitats = st.session_state.unitats_df.unitat.unique().tolist()
        help_message = "L'OPTIMITZADOR ENCARA NO HO SUPORTA. " \
                       "quines unitats ha portat altres anys? Omple abans la llista d'unitats"
        experience_col.multiselect(label='', options=current_unitats, on_change=insert_info,
                                   kwargs={'col_to_add': 'experience', 'col_to_match': 'cap', 'match': cap,
                                           'key': experience_key, 'table_name': 'caps_df'},
                                   key=experience_key, help=help_message, disabled=True)
