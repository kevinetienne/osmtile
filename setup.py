from distutils.core import setup

version = "0.1alpha"

setup(
    name = "osmtile",
    description = "Download a tile from osm (not very stable)",
    version = version,
    packages = ['osmtile',],
    long_description = open('README').read(),
)
