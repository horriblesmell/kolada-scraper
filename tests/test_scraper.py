# encoding: utf-8
from unittest import TestCase

from kolada import KoladaScraper


class TestKoladaScraper(TestCase):

    def setUp(self):
        self.scraper = KoladaScraper()

    def test_fetch_all_datasets(self):
        """Setting up scraper."""
        self.assertTrue(len(self.scraper.items))

    def test_get_munis(self):
        dataset = self.scraper.items["N10033"]
        towns = [x for x in dataset.dimensions['municipality'].allowed_values]
        self.assertTrue(len(towns) > 0)

    def test_query_by_period(self):
        dataset = self.scraper.items["N10033"]
        res = dataset.fetch({
            "period": 2016,
        })
        self.assertTrue(len(res.list_of_dicts) > 0)

    def test_query_by_region(self):
        dataset = self.scraper.items["N10033"]
        res = dataset.fetch({
            "municipality": ["0180"],
        })
        df = res.pandas.municipality
        self.assertTrue(len(res.list_of_dicts) > 0)
        self.assertTrue(df.nunique() == 1)
