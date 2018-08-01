import json
import os
import sys

try:
    from setuptools import setup
except ImportError as ex:
    from distutils.core import setup

with open("info.json") as infofile:
    infodict = json.load(infofile)

VERSION = infodict["VERSION"]
FORMAT_VERSION = infodict["FORMAT_VERSION"]
AUTHOR = infodict["AUTHOR"]
COPYRIGHT = infodict["COPYRIGHT"]
CONTACT = infodict["CONTACT"]
HOMEPAGE = infodict["HOMEPAGE"]
CLASSIFIERS = infodict["CLASSIFIERS"]


packages = ['converter']

with open('README.md') as f:
    description_text = f.read()

# nixio should be also listed here once the no-bindings version is available on pypi
install_req = ["odML",
	       "nixio==1.4.dev"] 

if sys.version_info < (3, 4):
    install_req += ["enum34"]

setup(
    name='nix-odML-converter',
    version=VERSION,
    description='Converter between NIX and odML format',
    author=AUTHOR,
    author_email=CONTACT,
    url=HOMEPAGE,
    packages=packages,
    test_suite='test',
    install_requires=install_req,
    include_package_data=True,
    long_description=description_text,
    classifiers=CLASSIFIERS,
    dependency_links = ['git+https://github.com/G-Node/nixpy.git@no-bindings-dev#egg=nixio-1.4.dev'],
    license="BSD"
)
