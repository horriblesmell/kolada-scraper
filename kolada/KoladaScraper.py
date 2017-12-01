# encoding: utf-8
import math

from statscraper import BaseScraper, Dataset, Dimension, Result, DimensionValue
import numpy as np
import requests

class KoladaScraper(BaseScraper):
    """Sample scraper for statscraper boilerplate."""

    def _fetch_itemslist(self, item):
        """Yield a collection or dataset at
        the current cursor position."""
        self.base_url = 'http://api.kolada.se/v2/'
        r = requests.get(self.base_url + '/kpi')
        data = r.json()
        for d in data['values']:
            yield Dataset(d['id'], label=d['title'], blob=d) # blob (data)

    def _fetch_dimensions(self, dataset):
        """Yield the available dimensions in <dataset>."""
        yield Dimension('municipality', label='municipality')
        yield Dimension('kpi', label='indicator')
        yield Dimension('gender', label='gender')
        yield Dimension('period', label='period')

    def _fetch_allowed_values(self, dimension):
        """Yield the allowed values for <dimension>."""
        if dimension.dataset.blob['municipality_type'] is 'K':
            data = requests.get(self.base_url + '/municipality').json()
            towns = [row['id'] for row in data['values']]
            yield DimensionValue(towns,
                                dimension,
                                label='Swedish municipalities')

    def _fetch_data(self, dataset, query=None):
        """Yield rows from <dataset>."""

        query_ = self.chunkify(query, 'municipality')

        for idx, q_ in enumerate(query_):
            for i, v in q_.items():
                try:
                    query_[idx][i] = ','.join(v)
                except TypeError:
                    query_[idx][i] = ','.join(str(x) for x in v)

        data = []
        for q in query_:
            url = '{}/data/kpi/{}/municipality/{}/year/{}'.format(
                self.base_url,
                dataset.id,
                q['municipality'],
                q['period']
            )
            r = requests.get(url)
            data.append(r.json())

        for res in data:
            for mun in res['values']:
                for d in mun['values']:
                    yield Result(d['value'], {
                            'kpi': dataset.label,
                            'gender': d['gender'],
                            'municipality': mun['municipality'],
                            'period': mun['period']
                        }
                    )

    def chunkify(self, q, k):
        res = []
        for i in np.array_split(q[k], math.ceil(len(q[k]) / 5)):
            q_ = {**q}
            q_[k] = list(i)
            res.append(q_)
        return res
