# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='notify_me',
    version='0.1.0',
    description='Bus notification system',
    long_description=readme,
    author='Diego López',
    author_email='dlopez@ets.es',
    packages=find_packages(exclude=('tests', 'docs'))
)