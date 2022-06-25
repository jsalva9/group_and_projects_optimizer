import pandas as pd

from config import Config
from data_transform.data_control import DataControl
from optimizer.optimizer import Optimizer


if __name__ == '__main__':
    config = Config()

    data_control = DataControl(config)
    raw_inputs = {
        'caps_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/caps_df.csv'),
        'unitats_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/unitats_df.csv'),
        'caps_preferences_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/caps_preferences_df.csv'),
        'unitats_preferences_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/unitats_preferences_df.csv'),
        'fixed_caps_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/fixed_caps.csv')
    }
    fixed_caps = {unitat: [] for unitat in raw_inputs['unitats_df'].unitat.unique().tolist()}
    for col in raw_inputs['fixed_caps_df'].columns:
        cap = str(col)
        if cap not in raw_inputs['caps_df'].cap.unique().tolist():
            continue
        unitat = raw_inputs['fixed_caps_df'].loc[0, col]
        fixed_caps[unitat].append(cap)
    raw_inputs['fixed_caps'] = fixed_caps

    data_control.set_raw_inputs(raw_inputs)
    data_control.transform_from_app_inputs()
    data_control.write_transformed()

    optimizer = Optimizer(config, data_control.transformed_inputs)
    solution = optimizer.run()
    solution.print_equips()
    by_cap, by_unitat = solution.get_stats()
    print()
