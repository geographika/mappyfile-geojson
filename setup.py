import re
from setuptools import setup
from io import open

(__version__,) = re.findall('__version__ = "(.*)"', open("mappyfile_geojson.py").read())


def readme():
    with open("README.rst", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="mappyfile-geojson",
    version=__version__,
    description="A mappyfile plugin to convert GeoJSON to inline Mapfile features",
    long_description=readme(),
    long_description_content_type="text/x-rst",
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
    ],
    url="http://github.com/geographika/mappyfile-geojson",
    author="Seth Girvin",
    author_email="sethg@geographika.co.uk",
    license="MIT",
    py_modules=["mappyfile_geojson"],
    install_requires=["geojson>=3.0.0"],
    entry_points={"mappyfile.plugins": "mappyfile_geojson = mappyfile_geojson"},
    zip_safe=False,
)
