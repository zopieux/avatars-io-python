#!/usr/bin/env python

# Copyright 2008-2012 Alexandre `Zopieux` Macabies
# This file was borrowed from shazow/urllib3

from distutils.core import setup

import os
import re

try:
    import setuptools
except ImportError:
    pass

base_path = os.path.dirname(__file__)

fp = open(os.path.join(base_path, 'avatarsio', '__init__.py'))
VERSION = re.compile(r".*__version__ = '(.*?)'",
                     re.S).match(fp.read()).group(1)
fp.close()

version = VERSION

requirements = ['requests',]

setup(name='avatarsio',
      version=version,
      description="Avatar picker and uploader for Avatars.io",
      long_description=open('README.md').read(),
      classifiers=[
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Software Development :: Libraries',
      ],
      keywords='avatars avatarsio twitter facebook instagram gravatar',
      author='Alexandre `Zopieux` Macabies',
      author_email='web@zopieux.com',
      url='https://github.com/Zopieux/avatars-io-python',
      license='MIT',
      packages=['avatarsio',],
      requires=requirements,
)
