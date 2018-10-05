#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open('README.md') as handle:
    LONG_DESCRIPTION = handle.read()

with open('VERSION') as handle:
    VERSION = handle.read().strip()

REQUIREMENTS = [
    'ansible',
    'pytest-ansible',
    'pytest',
    'unittest2',
]

setup(
    name='testfm',
    version=VERSION,
    description='TestFM is a test suite which exercises foreman-maintain tool.',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/SatelliteQE/testfm',
    author='Nikhil Kathole',
    author_email='nikhilkathole2683@gmail.com',
    license='GNU GPL v3.0',
    classifiers=[
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU General Public License v3 or later '
         '(GPLv3+)'),
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(exclude=['docs']),
    install_requires=REQUIREMENTS,
)
