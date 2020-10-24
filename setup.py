#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file based on https://github.com/kennethreitz/setup.py/blob/master/setup.py

# From https://packaging.python.org/discussions/install-requires-vs-requirements/#requirements-files :
#
# Whereas install_requires defines the dependencies for a single project,
# requirements files are often used to define the requirements for a complete Python environment.
# Whereas install_requires requirements are minimal,
# requirements files often contain an exhaustive listing of pinned versions for the purpose of achieving
# repeatable installations of a complete environment.
#
import os

from setuptools import setup, find_packages

# Package meta-data.
NAME = 'boggle'
DESCRIPTION = 'Boggle word finder'
# URL = 'https://github.com/me/myproject'
EMAIL = 'arthurstreet@yahoo.com'
AUTHOR = 'Arthur Street'

# What packages are required for this module to be executed?
REQUIRED = []

# You can install using eg. `pip install boggle[dev]==1.0.1`.
EXTRAS = {
    'dev': ['pytest-cov', 'pytest', 'hypothesis', 'mypy', 'radon', 'pycodestyle'],
}

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
# with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
#     long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about: dict = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    # long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    # url=URL,
    packages=find_packages(exclude=('scripts', 'test_utilities')),
    # packages=find_packages(exclude=('tests',)),
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    package_data={'boggle': ['LICENSE.txt',]},
    license='Unknown',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: Other/Proprietary License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    # $ setup.py publish support.
    # cmdclass={
    #     'upload': UploadCommand,
    # },
)
