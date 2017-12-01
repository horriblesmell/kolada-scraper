# encoding: utf-8
from setuptools import setup

def readme():
    """Import README for use as long_description."""
    with open("README.rst") as f:
        return f.read()

version = "0.0.1"

setup(
    name="kolada_scraper",
    version=version,
    description="A scraper of statistical data from api.kolada.se/v2 built on top of Statscraper.",
    long_description=readme(),
    url="https://github.com/horriblesmell/kolada-scraper",
    author="Sascha Granberg",
    author_email="saschagranberg.jobb@gmail.com",
    license="MIT",
    packages=["kolada"],
    zip_safe=False,
    install_requires=[
        "requests",
    ],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
    download_url="https://github.com/horriblesmell/kolada-scraper/archive/%s.tar.gz"
                 % version,
)
