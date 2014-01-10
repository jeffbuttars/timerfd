#!/usr/bin/env python
# encoding: utf-8

# from setuptools import setup, Extension, find_packages
from setuptools import setup, Extension


setup(
    version="0.1",
    description="FD timer for python",
    url='https://github.com/jeffbuttars/timerfd',
    # long_description=(open('README.md').read()),
    author="Jeff Buttars",
    author_email="jeff@jeffbuttars.com",
    license='MIT',
    ext_modules=[Extension('timerfd', sources=['timerfd/timerfd.c'])],
)
