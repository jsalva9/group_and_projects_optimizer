import pandas as pd

from typing import Tuple, Dict, List

from optimizer.solution import Solution
from optimizer.data_model import DataModel

from ortools.sat.python import cp_model


class Optimizer:

    def __init__(self, config, inputs):
        self._config = config

        self._data_model = DataModel(**inputs)
        self._data_model.create_data_model()

    def run(self) -> Solution:
        print(f'Running optimizer...')
        model = cp_model.CpModel()

        x, y = self.define_variables(model)
        self.define_constraints(model, x, y)
        self.define_objective_function(model, x, y)
        happiness_stats, solution_values = self.solve(model, x, y)
        solution_table = self.extract_solution(solution_values, happiness_stats)

        solution = Solution(solution_table)
        solution.print_equips()
        solution.print_stats()

        return solution

    def extract_solution(self, solution_values, happiness_stats) -> pd.DataFrame:
        solution = pd.DataFrame()
        for (i, k), value in solution_values.items():
            if value == 1:
                row = pd.DataFrame({
                    'cap_id': [i],
                    'unitat_id': [k]
                })
                solution = pd.concat([solution, row])

        solution = solution.merge(self._data_model.master_caps, how='left', on='cap_id').merge(
            self._data_model.master_unitats, how='left', on='unitat_id')

        solution['happiness'] = solution['cap_id'].apply(lambda id: happiness_stats[id])
        return solution

    def solve(self, model, x, y) -> Tuple[Dict[int, float], Dict[Tuple[int, int], int]]:
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        translated_status = 'OPTIMAL' if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE else 'INFEASIBLE'
        print(f'-- {translated_status} solution --')

        happiness_stats, solution_values = self.evaluate_expressions(solver, x, y)

        return happiness_stats, solution_values

    def evaluate_expressions(self, solver, x: dict, y: dict) -> Tuple[Dict[int, float], Dict[Tuple[int, int], int]]:
        solution_values = {key: solver.Value(value) for key, value in x.items()}
        equips = {i: [y[i, j, k] * self._data_model.caps_cost[i, j] for j in self._data_model.cap_ids for k in
                      self._data_model.unitat_ids] for i in self._data_model.cap_ids}
        unitats = {i: [x[i, k] * self._data_model.unitats_cost[i, k]
                       for k in self._data_model.unitat_ids] for i in self._data_model.cap_ids}
        equip_de_caps_weight = self._config.optimization['equip_de_caps_weight']
        happiness_stats = {}
        for i in self._data_model.cap_ids:
            happiness = equip_de_caps_weight * sum(equips[i]) + (1 - equip_de_caps_weight) * sum(unitats[i])
            happiness_stats[i] = happiness if type(happiness) in [float, int] else solver.Value(happiness)
        return happiness_stats, solution_values

    def define_objective_function(self, model, x: dict, y: dict) -> None:
        # TODO: introduir una FO alternativa per distribuir happiness equivalentment
        # Happiness of caps in relation to equip de caps
        equips = [y[i, j, k] * self._data_model.caps_cost[i, j]
                  for i in self._data_model.cap_ids
                  for j in self._data_model.cap_ids
                  for k in self._data_model.unitat_ids]
        # Happiness of caps in relation to unitat
        unitats = [x[i, k] * self._data_model.unitats_cost[i, k]
                   for i in self._data_model.cap_ids
                   for k in self._data_model.unitat_ids]
        equip_de_caps_weight = self._config.optimization['equip_de_caps_weight']
        model.Maximize(equip_de_caps_weight * sum(equips) + (1 - equip_de_caps_weight) * sum(unitats))

    def define_constraints(self, model, x: dict, y: dict) -> None:
        # Una unitat per cap
        for i in self._data_model.cap_ids:
            model.Add(sum([x[i, k] for k in self._data_model.unitat_ids]) == 1)
        # Min i max de caps per unitat
        for k in self._data_model.unitat_ids:
            model.Add(sum([x[i, k] for i in self._data_model.cap_ids]) >= self._data_model.min_caps[k])
            model.Add(sum([x[i, k] for i in self._data_model.cap_ids]) <= self._data_model.max_caps[k])
        # TODO: Dues persones no van juntes
        # TODO: Dues persones si que van juntes
        # TODO: Un mínim d'experiència per equip

    def define_variables(self, model) -> Tuple[dict, dict]:
        x = {}
        for cap_id in self._data_model.cap_ids:
            for unitat_id in self._data_model.unitat_ids:
                x[(cap_id, unitat_id)] = model.NewBoolVar(f'x_{cap_id}_{unitat_id}')
        y = {}
        for i in self._data_model.cap_ids:
            for j in self._data_model.cap_ids:
                for k in self._data_model.unitat_ids:
                    y[(i, j, k)] = model.NewBoolVar(f'y_{i}_{j}_{k}')
                    model.Add(y[i, j, k] <= x[i, k])
                    model.Add(y[i, j, k] <= x[j, k])
                    model.Add(y[i, j, k] >= x[i, k] + x[j, k] - 1)
        return x, y
