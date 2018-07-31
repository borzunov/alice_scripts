#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup


project_dir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(project_dir, 'alice_scripts', '__init__.py')) as f:
    version = re.search(r"__version__ = '(.+)'", f.read()).groups()[0]

with open(os.path.join(project_dir, 'README.md')) as f:
    long_description = f.read()

setup(
    name='alice_scripts',
    version=version,
    packages=['alice_scripts'],

    install_requires=['Flask>=0.12.2', 'pymorphy2>=0.8', 'werkzeug>=0.14.1'],

    author='Alexander Borzunov',
    author_email='borzunov.alexander@gmail.com',

    description='Simple way to create complex scripts for Yandex.Alice',
    long_description=long_description,
    url='http://github.com/borzunov/alice_scripts',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: AsyncIO',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    license='MIT',
    keywords=['yandex-alice'],
)
