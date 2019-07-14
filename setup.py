#!/usr/bin/env python

from distutils.core import setup

with open('README.md') as readme_file:
    long_description = readme_file.read()

setup(name='bp',
      version='0.3.0',
      description='CLI tool for recording the blood pressure',
      long_description=long_description,
      author='Kazufumi Ohkawa',
      author_email='kerolinq@gmail.com',
      url='https://github.com/kzfm/bp',
      packages=['.'],
      install_requires=['click'],
      entry_points={
          'console_scripts':['bp=bp:cmd'],
        },
      license='MIT',
     )
