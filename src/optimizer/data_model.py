import pandas as pd


class DataModel:
    def __init__(self, config, master_caps, master_unitats,
                 preferences_caps, preferences_unitats):
        self._config = config

        self._master_caps = master_caps
        self._master_unitats = master_unitats
        self._preferences_caps = preferences_caps
        self._preferences_unitats = preferences_unitats

        self._cap_ids = {}
        self._unitat_ids = {}
        self._caps_cost = {}
        self._unitats_cost = {}
        self._min_caps = {}
        self._max_caps = {}
        self._year = {}
        self._fixed_unitat = {}
        self._male = {}
        self._female = {}
        self._year_indicator = {}
        self._unitats_vetades_by_year = {}

    def create_data_model(self):
        self._cap_ids = self._master_caps.cap_id.values.tolist()
        self._unitat_ids = self._master_unitats.unitat_id.values.tolist()

        for row in self._preferences_caps.itertuples():
            self._caps_cost[(row.cap_id, row.cap_to_evaluate_id)] = row.preference

        for row in self._preferences_unitats.itertuples():
            self._unitats_cost[(row.cap_id, row.unitat_to_evaluate_id)] = row.preference

        years = self._master_caps.year.unique().tolist()
        self._year_indicator = {(cap_id, year): 0 for cap_id in self._cap_ids for year in years}

        for row in self._master_caps.itertuples():
            self._year[row.cap_id] = row.year
            self._male[row.cap_id] = 1 if row.gender == 'Masculí' else 0
            self._female[row.cap_id] = 1 if row.gender == 'Femení' else 0
            self._year_indicator[row.cap_id, row.year] = 1
            if not pd.isnull(row.fixed_unitat_id):
                self._fixed_unitat[row.cap_id] = row.fixed_unitat_id

        for row in self._master_unitats.itertuples():
            self._min_caps[row.unitat_id] = row.min_caps
            self._max_caps[row.unitat_id] = row.max_caps

        for year, unitats_vetades in self._config.optimization['unitats_vetades_by_year'].items():
            year = int(year)
            self._unitats_vetades_by_year[year] = [
                self._master_unitats.loc[self._master_unitats.unitat == unitat, 'unitat_id'].iloc[0] for unitat in
                unitats_vetades]

    @property
    def cap_ids(self):
        return self._cap_ids

    @property
    def unitat_ids(self):
        return self._unitat_ids

    @property
    def caps_cost(self):
        return self._caps_cost

    @property
    def unitats_cost(self):
        return self._unitats_cost

    @property
    def min_caps(self):
        return self._min_caps

    @property
    def max_caps(self):
        return self._max_caps

    @property
    def year(self):
        return self._year

    @property
    def master_caps(self):
        return self._master_caps

    @property
    def master_unitats(self):
        return self._master_unitats

    @property
    def fixed_unitat(self):
        return self._fixed_unitat

    @property
    def male(self):
        return self._male

    @property
    def female(self):
        return self._female

    @property
    def year_indicator(self):
        return self._year_indicator

    @property
    def unitats_vetades_by_year(self):
        return self._unitats_vetades_by_year
