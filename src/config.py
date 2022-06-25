import json
from pathlib import Path
import yaml


class Config:
    """Execution and algorithm configuration"""

    def __init__(self):
        root_path = self.get_project_root()
        config_filepath = f'{root_path}/config.yaml'
        self.__config = self.read_config(config_filepath, use_yaml=True)

        # self.__config = {
        #     'execution': {'etl': True, 'optimizer': True},
        #     'directories': {'data': 'data', 'raw': 'raw', 'transformed': 'transformed', 'output': 'output'},
        #     'file_names': {
        #         'preferences': 'Respostes formulari de la tria de caps - Respostes al formulari 1.csv',
        #         'master': 'master.xlsx'
        #     },
        #     'optimization': {'equip_de_caps_weight': .5}
        # }

        self.__directories = self.__config["directories"]
        self._data_directory = f'{root_path}/{self.__directories["data"]}'
        self._raw_data_directory = f'{self._data_directory}/{self.__directories["raw"]}'
        self._transformed_data_directory = f'{self._data_directory}/{self.__directories["transformed"]}'
        self._output_directory = f'{root_path}/{self.__directories["output"]}'

        self._execution = self.__config["execution"]
        self._file_names = self.__config["file_names"]
        self._optimization = self.__config["optimization"]

    @property
    def raw_data_directory(self):
        return self._raw_data_directory

    @property
    def transformed_data_directory(self):
        return self._transformed_data_directory

    @property
    def output_directory(self):
        return self._output_directory

    @property
    def execution(self):
        return self._execution

    @property
    def file_names(self):
        return self._file_names

    @property
    def optimization(self):
        return self._optimization


    @staticmethod
    def get_project_root() -> Path:
        """Get the project root filepath"""
        return Path(__file__).parent.parent

    @staticmethod
    def read_config(config_filepath, use_yaml=False) -> dict:
        """
        Read a configuration YAML file containing configuration parameters

        Args:
            config_filepath: string containing the file path
            use_yaml
        Returns:
            the config object
        """
        with open(config_filepath, "r") as config_file:
            if use_yaml:
                config_data = yaml.full_load(config_file)
            else:
                config_data = json.load(config_file)

        return config_data
