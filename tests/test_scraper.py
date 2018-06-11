# encoding: utf-8
from unittest import TestCase

from kolada import KoladaScraper


class TestKoladaScraper(TestCase):

    def setUp(self):
        self.scraper = KoladaScraper()

    def test_fetch_all_datasets(self):
        """Setting up scraper."""
        self.assertTrue(len(self.scraper.items))

    def test_fetch_munis(self):
        dataset = self.scraper.items["N10033"]
        towns = [x for x in dataset.dimensions['municipality'].allowed_values]
        self.assertTrue(len(towns) > 0)
