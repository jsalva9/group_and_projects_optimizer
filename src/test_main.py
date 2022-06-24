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
        'unitats_preferences_df': pd.read_csv(f'{config.raw_data_directory}/inputed_in_app/unitats_preferences_df.csv')
    }

    data_control.set_raw_inputs(raw_inputs)
    data_control.transform_from_app_inputs()

    optimizer = Optimizer(config, data_control.transformed_inputs)
    solution = optimizer.run()
    print()
