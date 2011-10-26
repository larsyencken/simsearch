# -*- coding: utf-8 -*-
#
#  setup.py
#  simsearch
#
#  Created by Lars Yencken on 2011-10-26.
#  Copyright 2011 Lars Yencken. All rights reserved.
#

"""
Package information for simsearch.
"""

from setuptools import setup
from setuptools.extension import Extension

setup(
    name='simsearch',
    author='Lars Yencken',
    author_email='lars@yencken.org',
    version='0.3.0',
    description='Similarity search for Japanese kanji.',
    url="http://simsearch.gakusha.info/",
    license='BSD',
    install_requires=[
        'cjktools>=1.5.0',
        'cjktools-data>=0.2.1-2010-07-29',
        'consoleLog>=0.2.4',
        'simplestats>=0.2.0',
        'pymongo',
        'mongoengine>=0.3',
        'pyyaml',
        'nltk',
        'mercurial',
        'flask',
        'simplejson',
    ],
    packages=['simsearch'],
    ext_modules=[Extension(
            'simsearch.stroke',
            sources=['simsearch/stroke.pyx'],
        )],
    scripts=['simsearch.py'],
    zip_safe=False,
)

