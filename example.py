from kolada import KoladaScraper

scraper = KoladaScraper()

dataset = scraper.items["N00002"] # pass a KPI id

data = dataset.fetch({
  'period': [2016, 2015]
})

print(data.pandas)
