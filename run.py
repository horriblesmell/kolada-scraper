#encoding:utf-8

from kolada import KoladaScraper
import dataset

TOPIC = 'N00002'
db = dataset.connect('sqlite:///koladadata.db')
table = db.create_table(TOPIC)

scraper = KoladaScraper()
data = scraper.items[TOPIC] # pass a KPI id
towns = [x.value for x in data.dimensions['municipality'].allowed_values]

res = data.fetch({
  'municipality': towns,
  'period': [2016, 2015]
})

table.insert_many(res.list_of_dicts)
