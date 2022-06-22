from config import Config
from data_transform.data_control import DataControl
from optimizer.optimizer import Optimizer


if __name__ == '__main__':
    config = Config()

    data_control = DataControl(config)
    if config.execution['etl']:
        data_control.read_data()
        data_control.transform()
        data_control.write_transformed()

    if config.execution['optimizer']:

        inputs = data_control.transformed_inputs if config.execution['etl'] else data_control.read_transformed()

        optimizer = Optimizer(config, inputs)
        solution = optimizer.run()

        data_control.write_output(solution)

    # TODO: interactive optimization. Very user friendly. Does not rely on google docs.
    # TODO: opti approach that defines a symmetric preferences matrix. Use the likelyhood that two people go together
    # TODO: dash / streamlit visualizer
