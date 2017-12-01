from kolada import KoladaScraper

scraper = KoladaScraper()

dataset = scraper.items["N00002"] # pass a KPI id

towns = [x.value for x in dataset.dimensions['municipality'].allowed_values]


data = dataset.fetch({
  'municipality': towns,
  'period': [2016, 2015]
})

print(data.pandas)
