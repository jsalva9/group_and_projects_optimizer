import pandas as pd
from typing import Tuple, Dict, List


class Solution:

    def __init__(self, solution_table: pd.DataFrame):
        self._solution_table = solution_table
        self._unitat_by_cap, self._equips_de_caps = self.define_teams(solution_table)

    @staticmethod
    def define_teams(solution_table) -> Tuple[Dict[str, str], Dict[str, List[str]]]:
        unitat_by_cap = {row.cap: row.unitat for row in solution_table.itertuples()}
        equips_de_caps = {
            unitat: [cap for cap in solution_table.cap.unique() if unitat_by_cap[cap] == unitat] for unitat in
            solution_table.unitat.unique().tolist()}
        return unitat_by_cap, equips_de_caps

    def print_equips(self) -> None:
        print('Equips de caps:')
        for key, val in self._equips_de_caps.items():
            print(f" - {key}: {', '.join(cap for cap in val)}")

    def print_stats(self) -> None:
        print('Happiness by cap:')
        by_cap = self._solution_table[['cap', 'unitat', 'happiness']].sort_values(by='happiness', ascending=False)
        by_cap['happiness_percent'] = by_cap['happiness'] / by_cap['happiness'].sum() * 100
        print(by_cap)

        print('Happiness by unitat:')
        by_unitat = self._solution_table.groupby(['unitat'], as_index=False).agg(
            team_happiness=('happiness', 'sum')).sort_values(by='team_happiness', ascending=False)
        by_unitat['happiness_percent'] = by_unitat['team_happiness'] / by_unitat['team_happiness'].sum() * 100
        print(by_unitat)

    @property
    def unitat_by_cap(self):
        return self._unitat_by_cap

    @property
    def equips_de_caps(self):
        return self._equips_de_caps

    @property
    def solution_table(self):
        return self._solution_table
