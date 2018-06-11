# encoding: utf-8
import math
from copy import deepcopy

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
        yield Dimension('kpi_label', label='indicator name')
        yield Dimension('gender', label='gender')
        yield Dimension('period', label='period')
        yield Dimension('status', label='status')

    def _fetch_allowed_values(self, dimension):
        """Yield the allowed values for <dimension>."""
        if dimension.dataset.blob['municipality_type'] == 'K':
            data = requests.get(self.base_url + '/municipality').json()
            towns = [(row['id'], row['title']) for row in data['values']]
            for town_id, town_name in towns:
                yield DimensionValue(town_id,
                                    dimension,
                                    label=town_name)

    def _fetch_data(self, dataset, query={}):
        """Make query for actual data.
        Get all regions and years by default.
        `period` (year) and `municipality` are the only implemented queryable
        dimensions.

        :param query: a dict with dimensions and values to query by.
            Examples:
            {"municipality": ["0180"]}
            {"period": 2016 }
        """
        #
        if "municipality" not in query and "period" not in query:
            query = {
                "municipality": [x.id for x in self.dimension["municipality"].allowed_values]
            }

        # Listify queried values (to allow single values in query, like {"year": 2016})
        for key, values in query.items():
            if not isinstance(values, list):
                query[key] = [values]
            # Format all values as strings for url creation
            query[key] = [str(x) for x in query[key]]

        # Validate query
        queryable_dims = ["municipality", "period"]
        for dim in query.keys():
            if dim not in queryable_dims:
                raise Exception("You cannot query on dimension '{}'".format(dim))
            #TODO: Make sure tha values passed in query are allowed.

        # base url for query
        next_url = '{}data/kpi/{}'.format(self.base_url, dataset.id)

        if "municipality" in query:
            next_url += "/municipality/{}".format(",".join(query["municipality"]))
        elif "period" in query:
            next_url += "/year/{}".format(",".join(query["period"]))

        while next_url:
            print("/GET {}".format(next_url))
            r = requests.get(next_url)
            r.raise_for_status()
            json_data = r.json()
            for row in json_data["values"]:
                for d in row["values"]:
                    yield Result(d['value'], {
                            'kpi': dataset.id,
                            'kpi_label': dataset.label,
                            'municipality': row['municipality'],
                            'period': row['period'],
                            'gender': d['gender'],
                            'status': d['status'],
                        }
                    )

            #
            if "next_page" in json_data:
                next_url = json_data["next_page"]
            else:
                next_url = False
