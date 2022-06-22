import os
import re

import pandas as pd

from config import Config
from optimizer.solution import Solution
from typing import Dict


class DataControl:

    def __init__(self, config: Config):
        self._config = config
        self._raw_inputs = None
        self._transformed_inputs = None

    def read_data(self):
        self._raw_inputs = {
            'master_caps': self.read_master('caps'),
            'master_unitats': self.read_master('unitats'),
            'preferences': self.read_preferences()
        }

    def read_master(self, master_table) -> pd.DataFrame:
        filepath = f"{self._config.raw_data_directory}/{self._config.file_names['master']}"
        return pd.read_excel(filepath, sheet_name=master_table)

    def read_preferences(self) -> pd.DataFrame:
        filepath = f"{self._config.raw_data_directory}/{self._config.file_names['preferences']}"
        return pd.read_csv(filepath)

    def transform(self):
        print(f'Running ETL...')
        master_caps = self._raw_inputs['master_caps']
        master_unitats = self._raw_inputs['master_unitats']
        preferences = self._raw_inputs['preferences']
        preferences = preferences.rename(columns={'Qui ets?': 'cap'}).drop(columns=['Marca de temps'])
        preferences.drop_duplicates(['cap'], keep='last', inplace=True)

        columns_to_rename = list(preferences.columns)
        columns_to_rename.remove('cap')
        new_names = [re.findall(r"\[([^]]*)\]", col)[0] for col in columns_to_rename]
        rename_dict = {a: b for (a, b) in zip(columns_to_rename, new_names)}

        preferences.rename(columns=rename_dict, inplace=True)

        caps_list = master_caps.cap.unique().tolist()
        unitats_list = master_unitats.unitat.unique().tolist()

        preferences_caps = preferences.drop(columns=unitats_list)
        preferences_unitats = preferences.drop(columns=caps_list)
        preferences_caps = pd.melt(preferences_caps, id_vars=['cap'], value_vars=caps_list, var_name='cap_to_evaluate',
                                   value_name='preference')
        preferences_unitats = pd.melt(preferences_unitats, id_vars=['cap'], value_vars=unitats_list,
                                      var_name='unitat_to_evaluate', value_name='preference')

        agg_preferences_caps = preferences_caps.groupby(['cap'], as_index=False).agg(
            total_allocated=('preference', 'sum'))
        preferences_caps = preferences_caps.merge(agg_preferences_caps, how='left', on='cap')
        preferences_caps['preference'] = preferences_caps['preference'] / preferences_caps['total_allocated']
        preferences_caps = preferences_caps.drop(columns=['total_allocated']).merge(
            master_caps, how='left', on='cap').merge(master_caps[['cap', 'id']], how='left', left_on='cap_to_evaluate',
                                                     right_on='cap')
        preferences_caps = preferences_caps.rename(
            columns={'cap_x': 'cap', 'id_x': 'cap_id', 'id_y': 'cap_to_evaluate_id'}).drop(columns=['cap_y'])
        preferences_caps.loc[preferences_caps.cap == preferences_caps.cap_to_evaluate, 'preference'] = 0

        agg_preferences_unitats = preferences_unitats.groupby(['cap'], as_index=False).agg(
            total_allocated=('preference', 'sum'))
        preferences_unitats = preferences_unitats.merge(agg_preferences_unitats, how='left', on='cap')
        preferences_unitats['preference'] = preferences_unitats['preference'] / preferences_unitats['total_allocated']
        preferences_unitats = preferences_unitats.drop(columns=['total_allocated']).merge(
            master_caps, how='left', on='cap').merge(master_unitats[['unitat', 'id']], how='left',
                                                     left_on='unitat_to_evaluate',
                                                     right_on='unitat')
        preferences_unitats = preferences_unitats.rename(
            columns={'id_x': 'cap_id', 'id_y': 'unitat_to_evaluate_id'}).drop(columns=['unitat'])

        master_caps.rename(columns={'id': 'cap_id'}, inplace=True)
        master_unitats.rename(columns={'id': 'unitat_id'}, inplace=True)

        self._transformed_inputs = {'preferences_unitats': preferences_unitats, 'preferences_caps': preferences_caps,
                                    'master_caps': master_caps, 'master_unitats': master_unitats}

    def write_transformed(self) -> None:
        for table_name, table in self._transformed_inputs.items():
            table.to_csv(f'{self._config.transformed_data_directory}/{table_name}.csv', index=False)

    def read_transformed(self) -> Dict[str, pd.DataFrame]:
        transformed_names = os.listdir(f'{self._config.transformed_data_directory}')
        self._transformed_inputs = {
            table_name[:-4]: pd.read_csv(f'{self._config.transformed_data_directory}/{table_name}') for table_name in
            transformed_names}
        return self._transformed_inputs

    def write_output(self, solution: Solution) -> None:
        solution.solution_table.to_csv(f'{self._config.output_directory}/solution.csv', index=False)

    @property
    def transformed_inputs(self) -> Dict[str, pd.DataFrame]:
        return self._transformed_inputs
