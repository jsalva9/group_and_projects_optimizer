import streamlit as st

from config import Config
from data_transform.data_control import DataControl
from optimizer.optimizer import Optimizer
from streamlit_app.utils import custom_write


def run_optimizer(scale_preferences=False):
    # TODO: introduir a algun lloc el tema scale preferences
    config = Config()
    data_control = DataControl(config)
    raw_inputs = {
        'caps_df': st.session_state.caps_df.copy(),
        'unitats_df': st.session_state.unitats_df.copy(),
        'caps_preferences_df': st.session_state.caps_preferences_df.copy(),
        'unitats_preferences_df': st.session_state.unitats_preferences_df.copy()
    }
    # for a, b in raw_inputs.items():
    #     st.write(a, b)
    data_control.set_raw_inputs(raw_inputs)
    data_control.transform_from_app_inputs()
    # for a, b in data_control.transformed_inputs.items():
    #     st.write(a, b)

    optimizer = Optimizer(config, data_control.transformed_inputs)
    solution = optimizer.run()
    return solution


def display_results(place, solution):
    columns = place.columns(len(solution.equips_de_caps))
    for i, col in enumerate(columns):
        columns[i].markdown(f'**{st.session_state.unitats[i]}**')
    for i, (unitat, equip) in enumerate(solution.equips_de_caps.items()):
        for cap in equip:
            columns[i].write(cap)


def opti_checks(place):
    some_caps = len(st.session_state.caps) > 0
    if not some_caps:
        place.warning('No hi ha caps introduïts')
    some_unitats = len(st.session_state.unitats) > 0
    if not some_unitats:
        place.warning('No hi ha unitats introduïdes')
    some_cap_cap_preference = st.session_state.caps_preferences_df.positive_preference.sum() > 0 or \
                              st.session_state.caps_preferences_df.negative_preference.sum() < 0
    if some_caps and not some_cap_cap_preference:
        place.warning('No hi ha preferències cap-cap')
    some_cap_unitat_preference = st.session_state.unitats_preferences_df.preference.sum() > 0
    if some_caps and some_unitats and not some_cap_unitat_preference:
        place.warning('No hi ha preferències cap-unitat')
    return some_caps and some_unitats and some_cap_cap_preference and some_cap_unitat_preference


def set_fixed_caps(key, unitat):
    st.session_state.fixed_caps[unitat] = st.session_state[key]


def optimizer():
    st.header('Resultats: equips de caps')
    save_to_csv = st.button('Save inputs to CSV (testing)')
    run_place = st.container()
    results_place = st.container()

    # TODO: remove, this is for testing purposes
    if save_to_csv:
        st.session_state.caps_df.to_csv(f'data/raw/inputed_in_app/caps_df.csv', index=False)
        st.session_state.unitats_df.to_csv(f'data/raw/inputed_in_app/unitats_df.csv', index=False)
        st.session_state.caps_preferences_df.to_csv(f'data/raw/inputed_in_app/caps_preferences_df.csv', index=False)
        st.session_state.unitats_preferences_df.to_csv(f'data/raw/inputed_in_app/unitats_preferences_df.csv',
                                                       index=False)

    # print_tables_for_debug()
    good_to_run = opti_checks(run_place)
    run_button = run_place.button('Fes els equips!')

    if len(st.session_state.unitats) == 0:
        return
    unitat_cols = results_place.columns(len(st.session_state.unitats))

    for i, unitat_col in enumerate(unitat_cols):
        # unitat_col.custom_write(st.session_state.unitat[i])
        unitat = st.session_state.unitats[i]
        fixed_caps_key = f'fixed_caps_{i}'
        available_caps = set(st.session_state.caps).difference(
            set([cap for u in st.session_state.unitats for cap in st.session_state.fixed_caps[u] if u != unitat]))
        unitat_col.multiselect(f'Caps fixats a {unitat}', options=available_caps, key=fixed_caps_key,
                               on_change=set_fixed_caps, kwargs={'unitat': unitat, 'key': fixed_caps_key},
                               default=st.session_state.fixed_caps[unitat])

    unitat_cols = results_place.columns(len(st.session_state.unitats))
    for i, unitat_col in enumerate(unitat_cols):
        unitat = st.session_state.unitats[i]
        custom_write(unitat_col, unitat, align='center', bold=True, auto_detect_color=True)
        for cap in st.session_state.fixed_caps[unitat]:
            custom_write(unitat_col, cap, align='center', color='black')


    # if run_button:
    #     if not good_to_run:
    #         run_place.error('Falten inputs per poder executar!')
    #     else:
    #         solution = run_optimizer()
    #         display_results(results_place, solution)

    def print_tables_for_debug():
        raw_inputs = {
            'caps_df': st.session_state.caps_df,
            'unitats_df': st.session_state.unitats_df,
            'caps_preferences_df': st.session_state.caps_preferences_df,
            'unitats_preferences_df': st.session_state.unitats_preferences_df
        }
        for a, b in raw_inputs.items():
            st.write(a, b)
