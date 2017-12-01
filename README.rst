This is a scraper for statistical data from http://api.kolada.se/v2/ built on top of the `Statscraper package <https://github.com/jplusplus/statscraper>`.

Install
-------

  pip install -r requirements.txt

Example usage
-------------

.. code:: python

  from kolada import KoladaScraper

  scraper = KoladaScraper()

  dataset = scraper.items['N00018']

  # Return a ValueList with all municipalities
  towns = dataset.dimensions['municipality'].allowed_values

  for town in towns:
      data = dataset.fetch({
          'municipality': town.value,
          'period': [2016, 2015]
      })

  print(data.pandas)

TODO
----

- Add more allowed values
- Implement errors when unallowed values are passed
- Implement regions
- Update `chunkify()` function, to make url building better
