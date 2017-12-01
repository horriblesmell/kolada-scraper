from kolada import KoladaScraper

scraper = KoladaScraper()

dataset = scraper.items['N00018'] # pass a KPI id

towns = dataset.dimensions['municipality'].allowed_values

for town in towns:
  data = dataset.fetch({
      'municipality': town.value,
      'period': [2016, 2015]
  })

print(data.pandas)
