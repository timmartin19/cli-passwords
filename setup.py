#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'keyring'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='cli-passwords',
    version='0.1.2',
    description="Makes securely getting, storing, and retrying passwords from a command line interface easy!",
    long_description=readme + '\n\n' + history,
    author="Tim Martin",
    author_email='tim@timmartin.me',
    url='https://github.com/timmartin19/cli_passwords',
    packages=[
        'cli_passwords',
    ],
    package_dir={'cli_passwords':
                 'cli_passwords'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='cli-passwords command line interface cli password retrieval keyring storage secure',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
