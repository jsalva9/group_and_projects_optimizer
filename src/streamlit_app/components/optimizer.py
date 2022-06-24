import streamlit as st

from config import Config
from data_transform.data_control import DataControl
from optimizer.optimizer import Optimizer


def run_optimizer(scale_preferences=False):
    # TODO: introduir a algun lloc el tema scale preferences
    config = Config()
    data_control = DataControl(config)
    raw_inputs = {
        'caps_df': st.session_state.caps_df,
        'unitats_df': st.session_state.unitats_df,
        'caps_preferences_df': st.session_state.caps_preferences_df,
        'unitats_preferences_df': st.session_state.unitats_preferences_df
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


def optimizer():
    st.header('Resultats: equips de caps')
    results_place = st.container()

    save_to_csv = st.button('Save to CSV')
    if save_to_csv:
        st.session_state.caps_df.to_csv(f'data/raw/inputed_in_app/caps_df.csv', index=False)
        st.session_state.unitats_df.to_csv(f'data/raw/inputed_in_app/unitats_df.csv', index=False)
        st.session_state.caps_preferences_df.to_csv(f'data/raw/inputed_in_app/caps_preferences_df.csv', index=False)
        st.session_state.unitats_preferences_df.to_csv(f'data/raw/inputed_in_app/unitats_preferences_df.csv', index=False)

    solution = run_optimizer()

    display_results(results_place, solution)


