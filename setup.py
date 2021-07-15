# -*- coding: utf-8 -*-

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

from distutils.core import setup

setup(name='Flows',
      version='0.0',
      description=readme,
      author='Ben Pine',
      author_email='bjpine@gmail.com',
      url='https://github.com/bjpine/flows',
      packages=['flows'],
     )